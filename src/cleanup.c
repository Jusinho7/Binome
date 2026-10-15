/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   cleanup.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/11 21:22:17 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/11 21:22:18 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	destroy_dongles(t_sim *sim)
{
	int	i;

	i = 0;
	while (i < sim->dongles_ready)
	{
		pthread_cond_destroy(&sim->dongles[i].cond);
		pthread_mutex_destroy(&sim->dongles[i].mutex);
		i++;
	}
}

static void	destroy_coders(t_sim *sim)
{
	int	i;

	i = 0;
	while (i < sim->coders_ready)
	{
		pthread_mutex_destroy(&sim->coders[i].lock);
		i++;
	}
}

void	destroy_sim(t_sim *sim)
{
	destroy_dongles(sim);
	destroy_coders(sim);
	free(sim->dongles);
	free(sim->coders);
	if (sim->locks_ready >= 1)
		pthread_mutex_destroy(&sim->stop_mutex);
	if (sim->locks_ready >= 2)
		pthread_mutex_destroy(&sim->log_mutex);
}
