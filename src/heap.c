/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/15 23:42:28 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/27 18:41:07 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	queue_req_less(t_queue *q, t_req *a, t_req *b)
{
	if (q->use_edf)
		return (edf_req_less(a, b));
	return (fifo_req_less(a, b));
}

static void	sift_up(t_queue *q, int index)
{
	int					parent;
	t_req				tmp;

	while (index > 0)
	{
		parent = (index - 1) / 2;
		if (!queue_req_less(q, &q->requests[index], &q->requests[parent]))
			break ;
		tmp = q->requests[index];
		q->requests[index] = q->requests[parent];
		q->requests[parent] = tmp;
		index = parent;
	}
}

static void	sift_down(t_queue *q, int index)
{
	int					left;
	int					best;
	t_req				tmp;

	while (1)
	{
		left = index * 2 + 1;
		if (left >= q->size)
			break ;
		best = left;
		if (left + 1 < q->size && queue_req_less(q, &q->requests[left + 1],
				&q->requests[left]))
			best = left + 1;
		if (!queue_req_less(q, &q->requests[best], &q->requests[index]))
			break ;
		tmp = q->requests[index];
		q->requests[index] = q->requests[best];
		q->requests[best] = tmp;
		index = best;
	}
}

void	queue_heap_add(t_queue *q, t_req req)
{
	q->requests[q->size] = req;
	q->size++;
	sift_up(q, q->size - 1);
}

void	queue_heap_remove_at(t_queue *q, int index)
{
	q->size--;
	if (index >= q->size)
		return ;
	q->requests[index] = q->requests[q->size];
	sift_down(q, index);
	sift_up(q, index);
}
