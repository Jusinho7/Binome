/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   lifo_scheduler.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/15 23:29:00 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/15 23:29:00 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	queue_set_lifo_policy(t_queue *q)
{
	q->use_lifo = 1;
}

int	lifo_queue_peek_id(t_queue *q)
{
	if (q->size == 0)
		return (-1);
	return (q->requests[q->size - 1].coder_id);
}
