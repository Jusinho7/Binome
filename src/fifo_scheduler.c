/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   fifo_policy.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/15 21:21:54 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/15 21:21:55 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	queue_set_fifo_policy(t_queue *q)
{
	q->use_edf = 0;
}

int	fifo_queue_peek_id(t_queue *q)
{
	if (q->size == 0)
		return (-1);
	return (q->requests[0].coder_id);
}
