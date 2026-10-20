/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/10 01:39:37 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/20 19:39:31 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	print_usage(void)
{
	fprintf(stderr, "\033[31mUsage: ./codexion number_of_coders "
		"time_to_burnout "
		"time_to_compile time_to_debug time_to_refactor "
		"number_of_compiles_required dongle_cooldown scheduler\n"
		"All values are positive integers (ms), "
		"scheduler is 'fifo' or 'edf'.\033[0m\n");
}

static int	parse_input(int argc, char **argv, t_sim *sim)
{
	if (!parse_args(argc, argv, sim))
	{
		print_usage();
		return (0);
	}
	return (1);
}

static int	start_simulation(t_sim *sim)
{
	if (!init_sim(sim) || !run_simulation(sim))
	{
		fprintf(stderr, "\033[31mError: simulation could not start\n\033[0m");
		return (0);
	}
	return (1);
}

int	main(int argc, char **argv)
{
	t_sim	sim;
	int		ret;

	memset(&sim, 0, sizeof(t_sim));
	if (!parse_input(argc, argv, &sim))
		return (1);
	ret = start_simulation(&sim);
	destroy_sim(&sim);
	return (ret);
}
