/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   run.c                                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/10 01:41:58 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/10 01:41:59 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	start_coders(t_sim *sim)
{
	int	i;

	i = 0;
	sim->start = now_ms();
	while (i < sim->n)
	{
		sim->coders[i].last_compile_start = sim->start;
		if (pthread_create(&sim->coders[i].thread, NULL,
				coder_routine, &sim->coders[i]) != 0)
			return (0);
		sim->coders_started++;
		i++;
	}
	return (1);
}

static void	join_coders(t_sim *sim)
{
	int	i;

	i = 0;
	while (i < sim->coders_started)
	{
		pthread_join(sim->coders[i].thread, NULL);
		i++;
	}
}

int	run_simulation(t_sim *sim)
{
	int	ok;

	ok = start_coders(sim);
	if (ok)
		ok = (pthread_create(&sim->monitor, NULL,
					monitor_routine, sim) == 0);
	if (ok)
		pthread_join(sim->monitor, NULL);
	else
	{
		set_stop(sim);
		wake_all(sim);
	}
	join_coders(sim);
	return (ok);
}
