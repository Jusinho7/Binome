/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/07 19:38:49 by srasolov          #+#    #+#             */
/*   Updated: 2026/09/07 21:24:36 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	dongle_init(t_dongle *d, int id)
{
	d->id = id;
	pthread_mutex_init(&d->lock, NULL);
	pthread_cond_init(&d->cond, NULL);
	d->in_use = 0;
	d->never_used = 1;
	d->free_since = 0;
	d->waiters = NULL;
}

static int	dongle_ready(t_dongle *d, t_waiter *w, t_sim *sim, long long now)
{
	t_waiter	*best;
	t_waiter	*cur;
	int			cooldown_ok;

	if (d->in_use || !d->waiters)
		return (0);
	cooldown_ok = d->never_used || now - d->free_since >= sim->dongle_cooldown;
	if (!cooldown_ok)
		return (0);
	best = d->waiters;
	cur = best->next;
	while (cur)
	{
		if (sim->scheduler == SCHED_EDF_MODE)
		{
			if (cur->deadline < best->deadline
				|| (cur->deadline == best->deadline
					&& cur->arrival < best->arrival))
				best = cur;
		}
		else if (cur->arrival < best->arrival)
			best = cur;
		cur = cur->next;
	}
	return (best == w);
}

static int	dongle_wait(t_dongle *d, t_waiter *w, t_sim *sim,
	struct timespec *ts)
{
	long long	wait_until;

	while (!sim_is_stopped(sim))
	{
		if (dongle_ready(d, w, sim, get_time_ms(sim)))
		{
			d->in_use = 1;
			d->never_used = 0;
			d->waiters = w->next;
			return (1);
		}
		if (!d->in_use && !d->never_used)
			wait_until = d->free_since + sim->dongle_cooldown;
		else
			wait_until = get_time_ms(sim) + 5;
		ms_to_abs_timespec(sim, wait_until, ts);
		pthread_cond_timedwait(&d->cond, &d->lock, ts);
	}
	return (0);
}

int	dongle_acquire(t_dongle *d, t_coder *c, t_sim *sim)
{
	t_waiter		w;
	struct timespec	ts;

	w.coder_id = c->id;
	w.arrival = get_time_ms(sim);
	w.deadline = c->last_compile_start + sim->time_to_burnout;
	pthread_mutex_lock(&d->lock);
	w.next = d->waiters;
	d->waiters = &w;
	if (dongle_wait(d, &w, sim, &ts))
	{
		pthread_mutex_unlock(&d->lock);
		return (1);
	}
	d->waiters = w.next;
	pthread_mutex_unlock(&d->lock);
	return (0);
}

void	dongle_release(t_dongle *d, t_sim *sim)
{
	pthread_mutex_lock(&d->lock);
	d->in_use = 0;
	d->free_since = get_time_ms(sim);
	pthread_cond_broadcast(&d->cond);
	pthread_mutex_unlock(&d->lock);
}
