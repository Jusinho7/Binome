/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/07 19:39:08 by srasolov          #+#    #+#             */
/*   Updated: 2026/09/07 21:19:31 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	sim_stop(t_sim *sim)
{
	pthread_mutex_lock(&sim->stop_lock);
	sim->stop = 1;
	pthread_mutex_unlock(&sim->stop_lock);
}

int	sim_is_stopped(t_sim *sim)
{
	int	v;

	pthread_mutex_lock(&sim->stop_lock);
	v = sim->stop;
	pthread_mutex_unlock(&sim->stop_lock);
	return (v);
}

static int	check_coder(t_sim *sim, int i)
{
	long long	now;
	int			burned;
	int			done;

	pthread_mutex_lock(&sim->coders[i].state_lock);
	now = get_time_ms(sim);
	burned = 0;
	if (sim->coders[i].state != STATE_COMPILING
		&& !sim->coders[i].burned_out
		&& now - sim->coders[i].last_compile_start > sim->time_to_burnout)
	{
		sim->coders[i].burned_out = 1;
		sim->coders[i].state = STATE_BURNED;
		burned = 1;
	}
	done = (sim->coders[i].compiles_done >= sim->n_compiles_required);
	pthread_mutex_unlock(&sim->coders[i].state_lock);
	if (burned)
		return (-1);
	return (done);
}

static int	monitor_step(t_sim *sim)
{
	int	i;
	int	done;
	int	all_done;

	i = 0;
	all_done = 1;
	while (i < sim->n_coders)
	{
		done = check_coder(sim, i);
		if (done == -1)
			return (-1);
		if (!done)
			all_done = 0;
		i++;
	}
	return (all_done);
}

void	*monitor_routine(void *arg)
{
	t_sim	*sim;
	int		status;

	sim = arg;
	while (!sim_is_stopped(sim))
	{
		usleep(1000);
		status = monitor_step(sim);
		if (status == -1)
		{
			log_event(sim, sim->coders[0].id, "burned out");
			sim_stop(sim);
			return (NULL);
		}
		if (status)
		{
			sim_stop(sim);
			return (NULL);
		}
	}
	return (NULL);
}
