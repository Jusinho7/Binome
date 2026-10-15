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

void	queue_init(t_queue *q)
{
	q->size = 0;
	q->use_edf = 0;
}

int	queue_add(t_queue *q, t_req req)
{
	int	i;

	i = 0;
	while (i < q->size)
	{
		if (q->requests[i].coder_id == req.coder_id)
			return (1);
		i++;
	}
	if (q->size >= DONGLE_QUEUE_CAPACITY)
		return (0);
	q->requests[q->size] = req;
	q->size++;
	return (1);
}

int	queue_remove(t_queue *q, int coder_id)
{
	int	i;

	i = 0;
	while (i < q->size)
	{
		if (q->requests[i].coder_id == coder_id)
		{
			while (i < q->size - 1)
			{
				q->requests[i] = q->requests[i + 1];
				i++;
			}
			q->size--;
			return (1);
		}
		i++;
	}
	return (0);
}

void	queue_capacity_error(t_sim *sim)
{
	fprintf(stderr,
		"\033[31mcodexion: dongle queue capacity exceeded\033[0m\n");
	set_stop(sim);
	wake_all(sim);
}
