/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_utils.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/30 14:19:45 by frazanak          #+#    #+#             */
/*   Updated: 2026/04/05 11:30:52 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	get_max_pos(t_list *stack_b)
{
	int	pos;
	int	max_pos;
	int	max_val;

	pos = 0;
	max_pos = 0;
	max_val = stack_b->value;
	while (stack_b)
	{
		if (stack_b->value > max_val)
		{
			max_val = stack_b->value;
			max_pos = pos;
		}
		pos++;
		stack_b = stack_b->next;
	}
	return (max_pos);
}

void	max_to_top_b(t_list **stack_b, t_options *opts)
{
	int	max_pos;
	int	size;

	max_pos = get_max_pos(*stack_b);
	size = ft_lstsize(*stack_b);
	if (max_pos <= size / 2)
		while (max_pos--)
			rotate_b(stack_b, opts->bench_mode, &opts->counters);
	else
	{
		max_pos = size - max_pos;
		while (max_pos--)
			reverse_b(stack_b, opts->bench_mode, &opts->counters);
	}
}

int	get_max_value(t_list *stack)
{
	int		max;
	t_list	*current;

	max = stack->value;
	current = stack;
	while (current)
	{
		if (current->value > max)
			max = current->value;
		current = current->next;
	}
	return (max);
}

int	get_min_value(t_list *stack)
{
	int		min;
	t_list	*current;

	min = stack->value;
	current = stack;
	while (current)
	{
		if (current->value < min)
			min = current->value;
		current = current->next;
	}
	return (min);
}

void	shift_values(t_list *stack, int offset)
{
	t_list	*current;

	current = stack;
	while (current)
	{
		current->value = current->value + offset;
		current = current->next;
	}
}
