/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/06 05:23:47 by srasolov          #+#    #+#             */
/*   Updated: 2026/09/30 10:39:07 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	main(int argc, char **argv)
{
	t_sim	sim;

	if (!parse_args(argc, argv, &sim))
	{
		fprintf(stderr, "\033[31mError: invalid arguments\033[0m\n");
		return (1);
	}
	if (!init_sim(&sim))
	{
		fprintf(stderr, "\033[31mError: initialization failed\33[0n\n");
		return (1);
	}
	printf("succes\n");
	gettimeofday(&sim.start_time, NULL);
	return (0);
}
