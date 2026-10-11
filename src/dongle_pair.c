/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle_pair.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/11 21:24:52 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/11 21:24:55 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

/*
** Priorite de cette demande (calculee UNE fois par "faim") :
**   edf  : la deadline du coder (debut du dernier compile + burnout)
**   fifo : l'heure d'arrivee en microsecondes (premier arrive = plus petit)
** Lecture de last_compile_start sans lock : seul le coder l'ecrit.
*/
static void	set_request_key(t_coder *c)
{
	struct timespec	ts;

	if (c->sim->use_edf)
		c->request_key = c->last_compile_start + c->sim->t_burnout;
	else
	{
		clock_gettime(CLOCK_MONOTONIC, &ts);
		c->request_key = ts.tv_sec * 1000000 + ts.tv_nsec / 1000;
	}
}

/*
** Essaie de prendre le 2e dongle SANS attendre. Reussit si le dongle est
** libre, hors cooldown, ET si personne de plus prioritaire n'est inscrit
** dans sa file. En cas d'echec on s'INSCRIT dans la file (une seule
** fois) : on garde ainsi notre rang pendant qu'on dort, et un coder
** moins prioritaire ne peut pas nous doubler. *seen memorise la
** "version" du dongle pour dormir jusqu'au prochain changement.
*/
static int	try_take(t_dongle *d, t_coder *c, long *seen, int *queued)
{
	t_req	mine;
	int		ok;

	mine.coder_id = c->id;
	mine.key = c->request_key;
	pthread_mutex_lock(&d->mutex);
	ok = (!d->in_use && now_ms() >= d->available_at);
	if (ok && d->queue.size > 0 && heap_peek_id(&d->queue) != c->id
		&& req_less(&d->queue.data[0], &mine))
		ok = 0;
	if (ok && *queued)
		heap_pop(&d->queue);
	if (ok)
		d->in_use = 1;
	else if (!*queued)
	{
		heap_push(&d->queue, mine);
		*queued = 1;
	}
	*seen = d->version;
	pthread_mutex_unlock(&d->mutex);
	return (ok);
}

/*
** Dort jusqu'a ce que le dongle change d'etat (version differente) ou
** que son cooldown se termine. On ne tient AUCUN dongle pendant ce temps.
*/
static void	wait_change(t_dongle *d, t_sim *sim, long seen)
{
	long			remaining;
	struct timespec	ts;

	pthread_mutex_lock(&d->mutex);
	while (d->version == seen && !is_stopped(sim))
	{
		remaining = d->available_at - now_ms();
		if (!d->in_use && remaining > 0)
		{
			make_abs_timeout(&ts, remaining);
			pthread_cond_timedwait(&d->cond, &d->mutex, &ts);
			break ;
		}
		pthread_cond_wait(&d->cond, &d->mutex);
	}
	pthread_mutex_unlock(&d->mutex);
}

/*
** Prend les 2 dongles "tout ou rien" :
**  1) on attend notre tour sur le 1er dongle (file prioritaire) ;
**  2) on essaie le 2e sans attendre ; si ca marche, on a les deux ;
**  3) sinon on REND le 1er, on s'inscrit dans la file du 2e (pour garder
**     notre rang) et on dort jusqu'a ce que le 2e bouge.
** On ne garde donc jamais un dongle en attendant l'autre : plus de
** "chaine" de coders bloques les uns derriere les autres, et le 1er
** dongle reste utilisable par un voisin pendant ce temps.
** Renvoie 0 si la simulation s'arrete (on ne tient alors rien).
*/
int	acquire_pair(t_coder *c)
{
	long	seen;
	int		queued;

	queued = 0;
	set_request_key(c);
	while (!is_stopped(c->sim))
	{
		if (!dongle_acquire(c->first, c))
			return (0);
		if (try_take(c->second, c, &seen, &queued))
			return (1);
		dongle_give_back(c->first);
		wait_change(c->second, c->sim, seen);
	}
	return (0);
}
