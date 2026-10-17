/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/10 01:22:45 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/17 22:52:30 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	init_one_dongle(t_dongle *d, t_sim *sim)
{
	d->in_use = 0;
	d->available_at = 0;
	d->version = 0;
	if (pthread_mutex_init(&d->mutex, NULL) != 0)
		return (0);
	if (pthread_cond_init(&d->cond, NULL) != 0)
	{
		pthread_mutex_destroy(&d->mutex);
		return (0);
	}
	if (!queue_init(&d->queue, sim->n))
	{
		pthread_cond_destroy(&d->cond);
		pthread_mutex_destroy(&d->mutex);
		return (0);
	}
	if (sim->use_edf)
		queue_set_edf_policy(&d->queue);
	else
		queue_set_fifo_policy(&d->queue);
	return (1);
}

static int	init_dongles(t_sim *sim)
{
	sim->dongles = malloc(sizeof(t_dongle) * sim->n);
	if (sim->dongles == NULL)
		return (0);
	while (sim->dongles_ready < sim->n)
	{
		if (!init_one_dongle(&sim->dongles[sim->dongles_ready], sim))
			return (0);
		sim->dongles_ready++;
	}
	return (1);
}

static int	init_coders(t_sim *sim)
{
	int	i;

	sim->coders = malloc(sizeof(t_coder) * sim->n);
	if (sim->coders == NULL)
		return (0);
	i = 0;
	while (i < sim->n)
	{
		if (pthread_mutex_init(&sim->coders[i].lock, NULL) != 0)
			return (0);
		sim->coders_ready++;
		if (sim->n == 1)
			set_single_coder(sim, i);
		else
			set_pair_coder(sim, i);
		i++;
	}
	return (1);
}

int	init_sim(t_sim *sim)
{
	sim->stop = 0;
	sim->dongles_ready = 0;
	sim->coders_ready = 0;
	sim->coders_started = 0;
	sim->locks_ready = 0;
	sim->dongles = NULL;
	sim->coders = NULL;
	if (pthread_mutex_init(&sim->stop_mutex, NULL) != 0)
		return (0);
	sim->locks_ready = 1;
	if (pthread_mutex_init(&sim->log_mutex, NULL) != 0)
		return (0);
	sim->locks_ready = 2;
	return (init_dongles(sim) && init_coders(sim));
}
