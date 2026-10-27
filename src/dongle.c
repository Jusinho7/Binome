/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/10 01:45:14 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/27 18:39:09 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	dongle_release(t_dongle *d, t_sim *sim)
{
	pthread_mutex_lock(&sim->table_mutex);
	d->in_use = 0;
	d->available_at = now_ms() + sim->cooldown;
	pthread_cond_broadcast(&sim->table_cond);
	pthread_mutex_unlock(&sim->table_mutex);
}

int	pair_free(t_coder *c, long t)
{
	return (!c->first->in_use && !c->second->in_use
		&& t >= c->first->available_at && t >= c->second->available_at);
}

int	pair_outranked(t_coder *c, t_dongle *d, long t)
{
	int		i;
	t_req	*r;

	i = 0;
	while (i < d->queue.size)
	{
		r = &d->queue.requests[i];
		if (r->coder_id != c->id
			&& queue_req_less(&d->queue, r, &c->pending)
			&& pair_free(&c->sim->coders[r->coder_id - 1], t))
			return (1);
		i++;
	}
	return (0);
}
