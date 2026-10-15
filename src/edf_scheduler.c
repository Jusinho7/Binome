/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   edf_scheduler.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/15 21:21:49 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/15 23:47:11 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	queue_set_edf_policy(t_queue *q)
{
	q->use_edf = 1;
}

int	edf_queue_peek_id(t_queue *q)
{
	if (q->size == 0)
		return (-1);
	return (q->requests[0].coder_id);
}

int	edf_req_less(t_req *a, t_req *b)
{
	if (a->key != b->key)
		return (a->key < b->key);
	return (a->coder_id < b->coder_id);
}

long	edf_request_key(t_coder *c)
{
	long	key;

	pthread_mutex_lock(&c->lock);
	key = c->last_compile_start + c->sim->t_burnout;
	pthread_mutex_unlock(&c->lock);
	return (key);
}
