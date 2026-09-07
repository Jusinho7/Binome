/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   cleanup.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/07 19:38:31 by srasolov          #+#    #+#             */
/*   Updated: 2026/09/07 21:24:11 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	dongle_destroy(t_dongle *d)
{
	pthread_mutex_destroy(&d->lock);
	pthread_cond_destroy(&d->cond);
}

void	free_sim(t_sim *sim)
{
	int	i;

	i = 0;
	while (i < sim->n_coders)
	{
		pthread_mutex_destroy(&sim->coders[i].state_lock);
		i++;
	}
	i = 0;
	while (i < sim->n_coders)
	{
		dongle_destroy(&sim->dongles[i]);
		i++;
	}
	pthread_mutex_destroy(&sim->print_lock);
	pthread_mutex_destroy(&sim->stop_lock);
	free(sim->coders);
	free(sim->dongles);
}
