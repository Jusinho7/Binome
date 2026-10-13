/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle_pair.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/11 21:24:52 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/13 17:38:50 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

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
