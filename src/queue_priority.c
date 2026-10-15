/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   queue_priority.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/15 22:23:00 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/15 22:23:00 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	queue_peek_id(t_queue *q)
{
	if (q->use_edf)
		return (edf_queue_peek_id(q));
	return (fifo_queue_peek_id(q));
}
