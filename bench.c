/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bench.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/03 12:10:00 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/05 12:27:06 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	set_bench_strategy(t_algo used_algo, char **strategy,
		char **complexity)
{
	if (used_algo == SIMPLE)
	{
		*strategy = "Simple";
		*complexity = "O(n²)";
	}
	else if (used_algo == MEDIUM)
	{
		*strategy = "Medium";
		*complexity = "O(n√n)";
	}
	else if (used_algo == COMPLEX)
	{
		*strategy = "Complex";
		*complexity = "O(n log n)";
	}
	else
	{
		*strategy = "Adaptive";
		*complexity = "O(n log n)";
	}
}

void	print_bench(int disorder, int n, t_algo used_algo, t_counters *counters)
{
	double	perc;
	char	*strategy;
	char	*complexity;
	int		total_ops;

	perc = (double)disorder / ((double)n * (n - 1) / 2) * 100;
	total_ops = counters->sa + counters->sb + counters->ss;
	total_ops += counters->pa + counters->pb + counters->ra;
	total_ops += counters->rb + counters->rr + counters->rra;
	total_ops += counters->rrb + counters->rrr;
	set_bench_strategy(used_algo, &strategy, &complexity);
	ft_printf_fd(2, "[bench] disorder:   %f%%\n", perc);
	ft_printf_fd(2, "[bench] strategy:   %s / %s\n", strategy, complexity);
	ft_printf_fd(2, "[bench] total_ops:  %d\n", total_ops);
	ft_printf_fd(2, "[bench] sa: %d  sb: %d  ss: %d  pa: %d  pb: %d\n",
		counters->sa, counters->sb, counters->ss, counters->pa, counters->pb);
	ft_printf_fd(2, "[bench] ra: %d  rb: %d  rr: %d  rra: %d\n", counters->ra,
		counters->rb, counters->rr, counters->rra);
	ft_printf_fd(2, "[bench] rrb: %d  rrr: %d\n", counters->rrb, counters->rrr);
}
