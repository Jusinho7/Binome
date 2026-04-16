/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_complex_utils.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: frazanak <frazanak@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/03 15:38:03 by frazanak          #+#    #+#             */
/*   Updated: 2026/04/03 15:38:03 by frazanak         ###   ########.fr       */
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
