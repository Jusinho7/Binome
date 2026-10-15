/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle_pair.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/11 21:24:52 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/14 06:24:04 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	set_request_key(t_coder *c)
{
	if (c->sim->use_edf)
		c->request_key = edf_request_key(c);
	else
		c->request_key = 0;
}

static int	queue_second_request(t_dongle *d, t_req req, int *queued)
{
	if (*queued)
		return (1);
	if (!queue_add(&d->queue, req))
		return (0);
	*queued = 1;
	return (1);
}

static int	try_acquire_dongle(t_dongle *d, t_coder *c, long *seen, int *queued)
{
	t_req	mine;
	int		ok;

	mine.coder_id = c->id;
	mine.key = c->request_key;
	pthread_mutex_lock(&d->mutex);
	if (!queue_second_request(d, mine, queued))
	{
		pthread_mutex_unlock(&d->mutex);
		queue_capacity_error(c->sim);
		return (0);
	}
	ok = (!d->in_use && now_ms() >= d->available_at
			&& queue_peek_id(&d->queue) == c->id);
	if (ok)
	{
		queue_remove(&d->queue, c->id);
		*queued = 0;
		d->in_use = 1;
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
		if (try_acquire_dongle(c->second, c, &seen, &queued))
			return (1);
		dongle_give_back(c->first);
		wait_change(c->second, c->sim, seen);
	}
	return (0);
}
