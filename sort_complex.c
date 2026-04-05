/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_complex.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/01 19:57:26 by frazanak          #+#    #+#             */
/*   Updated: 2026/04/03 12:37:31 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	get_max_bits(int max)
{
	int	bits;

	bits = 0;
	while ((max >> bits) != 0)
		bits++;
	return (bits);
}

static void	radix_pass(t_list **stack_a, t_list **stack_b, t_radix *radix,
		t_options *opts)
{
	int	i;

	i = 0;
	while (i < radix->size)
	{
		if ((((*stack_a)->value >> radix->bit) & 1) == 0)
			push_b(stack_a, stack_b, opts->bench_mode, &opts->counters);
		else
			rotate_a(stack_a, opts->bench_mode, &opts->counters);
		i++;
	}
}

static void	radix_sort(t_list **stack_a, t_list **stack_b, t_radix *radix,
		t_options *opts)
{
	while (radix->bit < radix->bits)
	{
		radix_pass(stack_a, stack_b, radix, opts);
		while (*stack_b)
			push_a(stack_b, stack_a, opts->bench_mode, &opts->counters);
		radix->bit++;
	}
}

void	sort_complex(t_list **stack_a, t_list **stack_b, t_options *opts)
{
	t_radix	radix;
	int		min;
	int		max;

	radix.size = ft_lstsize(*stack_a);
	if (radix.size <= 1)
		return ;
	min = get_min_value(*stack_a);
	if (min < 0)
		shift_values(*stack_a, -min);
	max = get_max_value(*stack_a);
	radix.bits = get_max_bits(max);
	radix.bit = 0;
	radix_sort(stack_a, stack_b, &radix, opts);
	if (min < 0)
		shift_values(*stack_a, min);
}
