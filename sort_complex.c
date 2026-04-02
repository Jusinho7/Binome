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

#include "push_swap.h"

static int	get_max_bits(t_list *stack)
{
	int		max;
	int		bits;

	max = stack->value;
	while (stack)
	{
		if (stack->value > max)
			max = stack->value;
		stack = stack->next;
	}
	bits = 0;
	while (max >> bits)
		bits++;
	return (bits);
}

static void	radix_pass(t_list **a, t_list **b, int bit)
{
	int		size;
	int		i;

	size = ft_lstsize(*a);
	i = 0;
	while (i < size)
	{
		if ((((*a)->value >> bit) & 1) == 0)
			push_b(a, b);
		else
			rotate_a(a);
		i++;
	}
	while (*b)
		push_a(b, a);
}

static void	normalize_stack(t_list **stack)
{
	int		size;
	int		*vals;
	int		i;
	int		j;
	int		tmp;

	size = ft_lstsize(*stack);
	vals = malloc(size * sizeof(int));
	if (!vals)
		return ;
	i = 0;
	while (i < size)
	{
		vals[i] = (*stack)->value;
		*stack = (*stack)->next;
		i++;
	}
	i = 0;
	while (i < size - 1)
	{
		j = 0;
		while (j < size - i - 1)
		{
			if (vals[j] > vals[j + 1])
			{
				tmp = vals[j];
				vals[j] = vals[j + 1];
				vals[j + 1] = tmp;
			}
			j++;
		}
		i++;
	}
	i = 0;
	while (i < size)
	{
		reverse_a(stack);
		i++;
	}
	i = 0;
	while (i < size)
	{
		j = 0;
		while (j < size)
		{
			if ((*stack)->value == vals[j])
			{
				(*stack)->value = j;
				break ;
			}
			j++;
		}
		*stack = (*stack)->next;
		i++;
	}
	free(vals);
}

void	sort_complex(t_list **a, t_list **b)
{
	int		bits;
	int		bit;

	normalize_stack(a);
	bits = get_max_bits(*a);
	bit = 0;
	while (bit < bits)
	{
		radix_pass(a, b, bit);
		bit++;
	}
}