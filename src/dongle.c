/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/10 01:45:14 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/10 01:45:15 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	can_take(t_dongle *d, t_coder *c)
{
	return (queue_peek_id(&d->queue) == c->id && !d->in_use);
}

static void	wait_turn(t_dongle *d, t_coder *c)
{
	long			remaining;
	struct timespec	ts;

	if (!can_take(d, c))
	{
		pthread_cond_wait(&d->cond, &d->mutex);
		return ;
	}
	remaining = d->available_at - now_ms();
	if (remaining > 0)
	{
		make_abs_timeout(&ts, remaining);
		pthread_cond_timedwait(&d->cond, &d->mutex, &ts);
	}
}

int	dongle_acquire(t_dongle *d, t_coder *c)
{
	t_req	req;

	req.coder_id = c->id;
	pthread_mutex_lock(&d->mutex);
	req.key = c->request_key;
	if (!queue_add(&d->queue, req))
	{
		pthread_mutex_unlock(&d->mutex);
		queue_capacity_error(c->sim);
		return (0);
	}
	while (!is_stopped(c->sim))
	{
		if (can_take(d, c) && now_ms() >= d->available_at)
		{
			queue_remove(&d->queue, c->id);
			d->in_use = 1;
			pthread_mutex_unlock(&d->mutex);
			return (1);
		}
		wait_turn(d, c);
	}
	pthread_mutex_unlock(&d->mutex);
	return (0);
}

void	dongle_release(t_dongle *d, t_sim *sim)
{
	pthread_mutex_lock(&d->mutex);
	d->in_use = 0;
	d->available_at = now_ms() + sim->cooldown;
	d->version++;
	pthread_cond_broadcast(&d->cond);
	pthread_mutex_unlock(&d->mutex);
}

void	dongle_give_back(t_dongle *d, t_sim *sim)
{
	pthread_mutex_lock(&d->mutex);
	d->in_use = 0;
	d->available_at = now_ms() + sim->cooldown;
	d->version++;
	pthread_cond_broadcast(&d->cond);
	pthread_mutex_unlock(&d->mutex);
}
