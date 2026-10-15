/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   queue.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/15 22:23:00 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/15 23:33:11 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	queue_peek_id(t_queue *q)
{
	if (q->use_edf)
		return (edf_queue_peek_id(q));
	return (fifo_queue_peek_id(q));
}

int	queue_init(t_queue *q, int capacity)
{
	q->requests = NULL;
	q->size = 0;
	q->capacity = capacity;
	q->use_edf = 0;
	q->next_order = 0;
	q->requests = malloc(sizeof(t_req) * (size_t)capacity);
	return (q->requests != NULL);
}

void	queue_destroy(t_queue *q)
{
	free(q->requests);
	q->requests = NULL;
}

int	queue_add(t_queue *q, t_req req)
{
	if (q->size >= q->capacity)
		return (0);
	req.order = q->next_order++;
	queue_heap_add(q, req);
	return (1);
}

int	queue_remove(t_queue *q, int coder_id)
{
	if (q->size == 0 || q->requests[0].coder_id != coder_id)
		return (0);
	queue_heap_remove(q);
	return (1);
}
