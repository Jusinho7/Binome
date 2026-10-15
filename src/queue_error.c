/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   queue_error.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/15 23:42:28 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/15 23:48:03 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	queue_capacity_error(t_sim *sim)
{
	fprintf(stderr,
		"\033[31mcodexion: dongle queue capacity exceeded\033[0m\n");
	set_stop(sim);
	wake_all(sim);
}
