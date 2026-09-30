/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/30 00:05:00 by srasolov          #+#    #+#             */
/*   Updated: 2026/09/30 10:26:01 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	heap_push(t_heap *h, t_waiter w)
{
	if (h->size >= 2)
		return ;
	h->data[h->size] = w;
	h->size++;
	heap_sift_up(h, h->size - 1);
}

t_waiter	heap_peek(t_heap *h)
{
	return (h->data[0]);
}

void	heap_pop(t_heap *h)
{
	h->size--;
	h->data[0] = h->data[h->size];
	if (h->size > 0)
		heap_sift_down(h, 0);
}

int	heap_remove(t_heap *h, int coder_id)
{
	int	i;

	i = 0;
	while (i < h->size && h->data[i].coder_id != coder_id)
		i++;
	if (i == h->size)
		return (0);
	h->size--;
	h->data[i] = h->data[h->size];
	heap_sift_up(h, i);
	heap_sift_down(h, i);
	return (1);
}
