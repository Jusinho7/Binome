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
		RED "codexion: dongle queue capacity exceeded" RESET "\n");
	set_stop(sim);
	wake_all(sim);
}
