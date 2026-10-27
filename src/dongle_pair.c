/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle_pair.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/11 21:24:52 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/27 18:32:37 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	pair_ready(t_coder *c, long t)
{
	return (pair_free(c, t)
		&& !pair_outranked(c, c->first, t)
		&& !pair_outranked(c, c->second, t));
}

static void	wait_pair(t_coder *c, long t)
{
	long			ready_at;
	struct timespec	ts;

	if (!c->first->in_use && !c->second->in_use)
	{
		ready_at = c->first->available_at;
		if (c->second->available_at > ready_at)
			ready_at = c->second->available_at;
		if (ready_at > t)
		{
			make_abs_timeout(&ts, ready_at - t);
			pthread_cond_timedwait(&c->sim->table_cond,
				&c->sim->table_mutex, &ts);
			return ;
		}
	}
	pthread_cond_wait(&c->sim->table_cond, &c->sim->table_mutex);
}

static int	enqueue_pair(t_coder *c)
{
	c->pending.coder_id = c->id;
	c->pending.key = c->request_key;
	c->pending.order = c->sim->next_order++;
	return (queue_add(&c->first->queue, c->pending)
		&& queue_add(&c->second->queue, c->pending));
}

static void	take_pair(t_coder *c)
{
	queue_remove(&c->first->queue, c->id);
	queue_remove(&c->second->queue, c->id);
	c->first->in_use = 1;
	c->second->in_use = 1;
}

int	acquire_pair(t_coder *c)
{
	t_sim	*sim;
	long	t;

	sim = c->sim;
	c->request_key = 0;
	if (sim->use_edf)
		c->request_key = edf_request_key(c);
	pthread_mutex_lock(&sim->table_mutex);
	if (!enqueue_pair(c))
	{
		pthread_mutex_unlock(&sim->table_mutex);
		return (queue_capacity_error(sim), 0);
	}
	t = now_ms();
	while (!is_stopped(sim) && !pair_ready(c, t))
	{
		wait_pair(c, t);
		t = now_ms();
	}
	if (is_stopped(sim))
		return (pthread_mutex_unlock(&sim->table_mutex), 0);
	take_pair(c);
	pthread_mutex_unlock(&sim->table_mutex);
	log_event(c, "has taken a dongle");
	return (log_event(c, "has taken a dongle"), 1);
}
