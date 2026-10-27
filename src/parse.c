/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parse.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/10 01:39:50 by srasolov          #+#    #+#             */
/*   Updated: 2026/10/27 19:12:14 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	parse_number(const char *s, long *out)
{
	long	value;
	int		i;

	i = 0;
	value = 0;
	if (s[0] == '\0')
		return (0);
	while (s[i] != '\0')
	{
		if (s[i] < '0' || s[i] > '9')
			return (0);
		value = value * 10 + (s[i] - '0');
		if (value > 2147483647)
			return (0);
		i++;
	}
	*out = value;
	return (1);
}

static int	parse_scheduler(const char *s, t_sim *sim)
{
	if (strcmp(s, "fifo") == 0)
	{
		sim->use_edf = 0;
		return (1);
	}
	if (strcmp(s, "edf") == 0)
	{
		sim->use_edf = 1;
		return (1);
	}
	return (0);
}

static void	set_values(t_sim *sim, long *v)
{
	sim->n = (int)v[0];
	sim->t_burnout = v[1];
	sim->t_compile = v[2];
	sim->t_debug = v[3];
	sim->t_refactor = v[4];
	sim->compiles_required = (int)v[5];
	sim->cooldown = v[6];
}

static void	cheick_value(long *v)
{
	if (v[0] < 1)
	{
		fprintf(stderr, RED "Error: nb_coders must be > 1\n" RESET);
		exit(1);
	}
	if (v[1] < 1)
	{
		fprintf(stderr, RED "Error: time_to_burnout must be > 0\n" RESET);
		exit(1);
	}
	if (v[2] < 1)
	{
		fprintf(stderr, RED "Error: time_to_compile must be > 0\n" RESET);
		exit(1);
	}
	if (v[5] < 1)
	{
		fprintf(stderr, RED "Error: number_of_compiles must be > 0\n" RESET);
		exit(1);
	}
}

int	parse_args(int argc, char **argv, t_sim *sim)
{
	long	v[7];
	int		i;

	if (argc != 9)
		return (0);
	i = 0;
	while (i < 7)
	{
		if (!parse_number(argv[i + 1], &v[i]))
			return (0);
		i++;
	}
	cheick_value(v);
	if (!parse_scheduler(argv[8], sim))
		return (0);
	set_values(sim, v);
	return (1);
}
