/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   state.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/10 01:41:26 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/27 18:43:21 by srasolov         ###   ########.fr       */
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
	pthread_mutex_lock(&sim->table_mutex);
	pthread_cond_broadcast(&sim->table_cond);
	pthread_mutex_unlock(&sim->table_mutex);
}

void	log_event(t_coder *c, const char *msg)
{
	t_sim		*sim;
	const char	*color;

	sim = c->sim;
	color = MAGENTA;
	if (strcmp(msg, "has taken a dongle") == 0)
		color = GREEN;
	else if (strcmp(msg, "is compiling") == 0)
		color = BLUE;
	else if (strcmp(msg, "is debugging") == 0)
		color = CYAN;
	pthread_mutex_lock(&sim->log_mutex);
	if (!is_stopped(sim))
		printf("%ld %d %s%s%s\n",
			now_ms() - sim->start, c->id, color, msg, RESET);
	pthread_mutex_unlock(&sim->log_mutex);
}

void	log_burnout(t_sim *sim, int id)
{
	pthread_mutex_lock(&sim->log_mutex);
	set_stop(sim);
	printf("%ld %d %sburned out%s\n",
		now_ms() - sim->start, id, ORANGE, RESET);
	pthread_mutex_unlock(&sim->log_mutex);
	wake_all(sim);
}
