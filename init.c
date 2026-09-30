/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/07 19:38:54 by srasolov          #+#    #+#             */
/*   Updated: 2026/09/30 10:32:30 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	init_coders(t_sim *sim, int i)
{
	sim->coders[i].id = i + 1;
	sim->coders[i].sim = sim;
	sim->coders[i].last_compile_start = 0;
	sim->coders[i].compiles_done = 0;
	sim->coders[i].state = STATE_IDLE;
	sim->coders[i].burned_out = 0;
	pthread_mutex_init(&sim->coders[i].state_lock, NULL);
	sim->coders[i].right = &sim->dongles[i];
	sim->coders[i].left = &sim->dongles[
		(i - 1 + sim->n_coders) % sim->n_coders];
}

static void	init_dongles(t_sim *sim, int i)
{
	t_dongle	*d;

	d = &sim->dongles[i];
	d->id = i;
	pthread_mutex_init(&d->lock, NULL);
	pthread_cond_init(&d->cond, NULL);
	d->in_use = 0;
	d->never_used = 1;
	d->free_since = 0;
	d->waiters.size = 0;
	d->waiters.mode = sim->scheduler;
}

static int	alloc_sim(t_sim *sim)
{
	sim->dongles = malloc(sizeof(t_dongle) * sim->n_coders);
	sim->coders = malloc(sizeof(t_coder) * sim->n_coders);
	if (!sim->dongles || !sim->coders)
	{
		free(sim->dongles);
		free(sim->coders);
		sim->dongles = NULL;
		sim->coders = NULL;
		return (0);
	}
	return (1);
}

static void	init_all(t_sim *sim)
{
	int	i;

	i = 0;
	while (i < sim->n_coders)
	{
		init_dongles(sim, i);
		i++;
	}
	i = 0;
	while (i < sim->n_coders)
	{
		init_coders(sim, i);
		i++;
	}
}

int	init_sim(t_sim *sim)
{
	if (!alloc_sim(sim))
		return (0);
	init_all(sim);
	pthread_mutex_init(&sim->print_lock, NULL);
	pthread_mutex_init(&sim->stop_lock, NULL);
	sim->stop = 0;
	return (1);
}
