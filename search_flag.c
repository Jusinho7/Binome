/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   search_flag.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/27 18:56:10 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/05 12:23:00 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	shift_argv(int *argc, char **argv, int start)
{
	while (start < *argc - 1)
	{
		argv[start] = argv[start + 1];
		start++;
	}
	argv[*argc - 1] = NULL;
	(*argc)--;
}

static t_algo	handle_algo_flag(int *argc, char **argv, int i)
{
	t_algo	result;

	result = check_flag(argv[i]);
	if (result != ADAPTIVE || ft_strcmp(argv[i], "--adaptive") == 0)
	{
		shift_argv(argc, argv, i);
		return (result);
	}
	return (ADAPTIVE);
}

t_algo	search_flag(int *argc, char **argv, int *bench_mode)
{
	t_algo	algo;
	int		i;

	algo = ADAPTIVE;
	i = 1;
	while (i < *argc)
	{
		if (ft_strcmp(argv[i], "--bench") == 0)
		{
			*bench_mode = 1;
			shift_argv(argc, argv, i);
			continue ;
		}
		algo = handle_algo_flag(argc, argv, i);
		if (algo != ADAPTIVE)
			break ;
		i++;
	}
	return (algo);
}
