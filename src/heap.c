/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/10 01:23:06 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/10 01:23:41 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	heap_init(t_heap *h, int cap)
{
	h->data = malloc(sizeof(t_req) * cap);
	if (h->data == NULL)
		return (0);
	h->size = 0;
	h->cap = cap;
	return (1);
}

void	heap_free(t_heap *h)
{
	free(h->data);
	h->data = NULL;
	h->size = 0;
}

int	heap_push(t_heap *h, t_req req)
{
	if (h->size >= h->cap)
		return (0);
	h->data[h->size] = req;
	h->size++;
	sift_up(h, h->size - 1);
	return (1);
}

t_req	heap_pop(t_heap *h)
{
	t_req	top;

	top = h->data[0];
	h->size--;
	h->data[0] = h->data[h->size];
	sift_down(h, 0);
	return (top);
}

int	heap_peek_id(t_heap *h)
{
	if (h->size == 0)
		return (-1);
	return (h->data[0].coder_id);
}
