/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_complex.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: frazanak <frazanak@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/01 19:57:26 by frazanak          #+#    #+#             */
/*   Updated: 2026/04/01 19:57:26 by frazanak         ###   ########.fr       */
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

static void	radix_pass(t_list **stack_a, t_list **stack_b, int bit, int size)
{
	int	i;

	i = 0;
	while (i < size)
	{
		if ((((*stack_a)->value >> bit) & 1) == 0)
			push_b(stack_a, stack_b);
		else
			rotate_a(stack_a);
		i++;
	}
}

static void	radix_sort(t_list **stack_a, t_list **stack_b, int bits, int size)
{
	int	bit;

	bit = 0;
	while (bit < bits)
	{
		radix_pass(stack_a, stack_b, bit, size);
		while (*stack_b)
			push_a(stack_b, stack_a);
		bit++;
	}
}

void	sort_complex(t_list **stack_a, t_list **stack_b)
{
	int	size;
	int	min;
	int	max;
	int	bits;

	size = ft_lstsize(*stack_a);
	if (size <= 1)
		return ;
	min = get_min_value(*stack_a);
	if (min < 0)
		shift_values(*stack_a, -min);
	max = get_max_value(*stack_a);
	bits = get_max_bits(max);
	radix_sort(stack_a, stack_b, bits, size);
	if (min < 0)
		shift_values(*stack_a, min);
}
