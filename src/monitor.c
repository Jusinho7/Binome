/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/08 18:44:46 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/10 00:53:05 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	is_burned_out(t_coder *c)
{
	long	deadline;

	pthread_mutex_lock(&c->lock);
	deadline = c->last_compile_start + c->sim->t_burnout;
	pthread_mutex_unlock(&c->lock);
	return (now_ms() >= deadline);
}

static int	has_finished(t_coder *c)
{
	int	count;

	pthread_mutex_lock(&c->lock);
	count = c->compile_count;
	pthread_mutex_unlock(&c->lock);
	return (count >= c->sim->compiles_required);
}

static int	scan_coders(t_sim *sim, int *all_done)
{
	int	i;

	i = 0;
	*all_done = 1;
	while (i < sim->n)
	{
		if (has_finished(&sim->coders[i]))
		{
			i++;
			continue ;
		}
		*all_done = 0;
		if (is_burned_out(&sim->coders[i]))
			return (i + 1);
		i++;
	}
	return (0);
}

void	*monitor_routine(void *arg)
{
	t_sim	*sim;
	int		dead;
	int		all_done;

	sim = (t_sim *)arg;
	while (1)
	{
		dead = scan_coders(sim, &all_done);
		if (dead != 0)
		{
			log_burnout(sim, dead);
			return (NULL);
		}
		if (all_done)
		{
			set_stop(sim);
			wake_all(sim);
			return (NULL);
		}
		usleep(500);
	}
	return (NULL);
}
