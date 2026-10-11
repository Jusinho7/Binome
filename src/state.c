/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   state.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/10 01:41:26 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/10 01:41:27 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	is_stopped(t_sim *sim)
{
	int	value;

	pthread_mutex_lock(&sim->stop_mutex);
	value = sim->stop;
	pthread_mutex_unlock(&sim->stop_mutex);
	return (value);
}

void	set_stop(t_sim *sim)
{
	pthread_mutex_lock(&sim->stop_mutex);
	sim->stop = 1;
	pthread_mutex_unlock(&sim->stop_mutex);
}

void	wake_all(t_sim *sim)
{
	int	i;

	i = 0;
	while (i < sim->n)
	{
		pthread_mutex_lock(&sim->dongles[i].mutex);
		pthread_cond_broadcast(&sim->dongles[i].cond);
		pthread_mutex_unlock(&sim->dongles[i].mutex);
		i++;
	}
}

void	log_event(t_coder *c, const char *msg)
{
	t_sim	*sim;

	sim = c->sim;
	pthread_mutex_lock(&sim->log_mutex);
	if (!is_stopped(sim))
		printf("%ld %d %s\n", now_ms() - sim->start, c->id, msg);
	pthread_mutex_unlock(&sim->log_mutex);
}

void	log_burnout(t_sim *sim, int id)
{
	pthread_mutex_lock(&sim->log_mutex);
	set_stop(sim);
	printf("%ld %d \033[38;5;208mburned out\033[0m\n", now_ms() - sim->start, id);
	pthread_mutex_unlock(&sim->log_mutex);
	wake_all(sim);
}
