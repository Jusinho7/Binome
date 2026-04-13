/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bench.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/03 12:10:00 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/13 14:48:12 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	set_bench_strategy(t_bench *bench, char **strategy,
		char **complexity)
{
	if (bench->algo == ADAPTIVE)
	{
		*strategy = "Adaptive";
		if (bench->n <= 5 || bench->perc < 20)
			*complexity = "O(n²)";
		else if (bench->perc < 50)
			*complexity = "O(n√n)";
		else
			*complexity = "O(n log n)";
	}
	else if (bench->algo == SIMPLE)
	{
		*strategy = "Simple";
		*complexity = "O(n²)";
	}
	else if (bench->algo == MEDIUM)
	{
		*strategy = "Medium";
		*complexity = "O(n√n)";
	}
	else if (bench->algo == COMPLEX)
	{
		*strategy = "Complex";
		*complexity = "O(n log n)";
	}
}

void	print_bench(int disorder, int n, t_algo algo, t_counters *counters)
{
	t_bench	bench;
	char	*strategy;
	char	*complexity;
	int		total_ops;

	bench.disorder = disorder;
	bench.n = n;
	bench.algo = algo;
	if (n > 1)
		bench.perc = (double)disorder / ((double)n * (n - 1) / 2) * 100;
	else
		bench.perc = 0;
	total_ops = counters->sa + counters->sb + counters->ss;
	total_ops += counters->pa + counters->pb + counters->ra;
	total_ops += counters->rb + counters->rr + counters->rra;
	total_ops += counters->rrb + counters->rrr;
	set_bench_strategy(&bench, &strategy, &complexity);
	ft_printf_fd(2, "[bench] disorder:   %f%%\n", bench.perc);
	ft_printf_fd(2, "[bench] strategy:   %s / %s\n", strategy, complexity);
	ft_printf_fd(2, "[bench] total_ops:  %d\n", total_ops);
	ft_printf_fd(2, "[bench] sa: %d  sb: %d  ss: %d  pa: %d  pb: %d\n",
		counters->sa, counters->sb, counters->ss, counters->pa, counters->pb);
	ft_printf_fd(2, "[bench] ra: %d  rb: %d  rr: %d  rra: %d\n", counters->ra,
		counters->rb, counters->rr, counters->rra);
	ft_printf_fd(2, "[bench] rrb: %d  rrr: %d\n", counters->rrb, counters->rrr);
}
