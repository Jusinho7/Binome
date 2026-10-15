/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/15 23:42:28 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/15 23:48:17 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	req_less(t_queue *q, t_req *a, t_req *b)
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
		if (!req_less(q, &q->requests[index], &q->requests[parent]))
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
		if (left + 1 < q->size && req_less(q, &q->requests[left + 1],
				&q->requests[left]))
			best = left + 1;
		if (!req_less(q, &q->requests[best], &q->requests[index]))
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

void	queue_heap_remove(t_queue *q)
{
	q->size--;
	if (q->size > 0)
	{
		q->requests[0] = q->requests[q->size];
		sift_down(q, 0);
	}
}
