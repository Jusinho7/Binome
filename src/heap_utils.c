/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap_utils.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/10 01:30:43 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/10 01:30:44 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	req_less(t_req *a, t_req *b)
{
	if (a->key != b->key)
		return (a->key < b->key);
	return (a->coder_id < b->coder_id);
}

static void	swap_req(t_req *a, t_req *b)
{
	t_req	tmp;

	tmp = *a;
	*a = *b;
	*b = tmp;
}

void	sift_up(t_heap *h, int i)
{
	int	parent;

	while (i > 0)
	{
		parent = (i - 1) / 2;
		if (!req_less(&h->data[i], &h->data[parent]))
			break ;
		swap_req(&h->data[i], &h->data[parent]);
		i = parent;
	}
}

void	sift_down(t_heap *h, int i)
{
	int	best;
	int	left;
	int	right;

	while (1)
	{
		best = i;
		left = 2 * i + 1;
		right = 2 * i + 2;
		if (left < h->size && req_less(&h->data[left], &h->data[best]))
			best = left;
		if (right < h->size && req_less(&h->data[right], &h->data[best]))
			best = right;
		if (best == i)
			break ;
		swap_req(&h->data[i], &h->data[best]);
		i = best;
	}
}
