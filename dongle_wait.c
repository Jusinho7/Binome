/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle_wait.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/01 00:10:29 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/01 00:55:07 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	dongle_ready(t_sim *sim, t_dongle *d, t_coder *coder)
{
	long long	now;

	if (d->in_use)
		return (0);
	now = get_now_ms(sim);
	if (!d->never_used && now < d->free_since + sim->dongle_cooldown)
		return (0);
	return (heap_peek(&d->waiters).coder_id == coder->id);
}

static void	compute_wake_ts(t_sim *sim, t_dongle *d, struct timespec *ts)
{
	long long	wake_at;
	long long	fallback;

	wake_at = d->free_since + sim->dongle_cooldown;
	fallback = get_now_ms(sim) + 20;
	if (wake_at < fallback)
		wake_at = fallback;
	ms_to_timespec(sim, wake_at, ts);
}

int	acquire_one(t_sim *sim, t_coder *coder, t_dongle *d)
{
	t_waiter		w;
	struct timespec	ts;

	pthread_mutex_lock(&d->lock);
	w.coder_id = coder->id;
	w.arrival = get_now_ms(sim);
	w.deadline = coder->last_compile_start + sim->time_to_burnout;
	heap_push(&d->waiters, w);
	while (!dongle_ready(sim, d, coder))
	{
		if (sim_is_stopped(sim))
		{
			heap_remove(&d->waiters, coder->id);
			pthread_mutex_unlock(&d->lock);
			return (0);
		}
		compute_wake_ts(sim, d, &ts);
		pthread_cond_timedwait(&d->cond, &d->lock, &ts);
	}
	heap_remove(&d->waiters, coder->id);
	d->in_use = 1;
	d->never_used = 0;
	pthread_mutex_unlock(&d->lock);
	return (1);
}
