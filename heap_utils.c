/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap_utils.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/30 01:20:30 by srasolov          #+#    #+#             */
/*   Updated: 2026/09/30 10:29:30 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	heap_is_better(t_heap *h, t_waiter *a, t_waiter *b)
{
	if (h->mode == SCHED_EDF_MODE)
	{
		if (a->deadline != b->deadline)
			return (a->deadline < b->deadline);
		return (a->coder_id < b->coder_id);
	}
	if (a->arrival != b->arrival)
		return (a->arrival < b->arrival);
	return (a->coder_id < b->coder_id);
}

void	heap_swap(t_waiter *a, t_waiter *b)
{
	t_waiter	tmp;

	tmp = *a;
	*a = *b;
	*b = tmp;
}

void	heap_sift_up(t_heap *h, int i)
{
	int	parent;

	while (i > 0)
	{
		parent = (i - 1) / 2;
		if (!heap_is_better(h, &h->data[i], &h->data[parent]))
			break ;
		heap_swap(&h->data[i], &h->data[parent]);
		i = parent;
	}
}

void	heap_sift_down(t_heap *h, int i)
{
	int	left;
	int	right;
	int	best;

	while (1)
	{
		left = 2 * i + 1;
		right = 2 * i + 2;
		best = i;
		if (left < h->size
			&& heap_is_better(h, &h->data[left], &h->data[best]))
			best = left;
		if (right < h->size
			&& heap_is_better(h, &h->data[right], &h->data[best]))
			best = right;
		if (best == i)
			break ;
		heap_swap(&h->data[i], &h->data[best]);
		i = best;
	}
}
