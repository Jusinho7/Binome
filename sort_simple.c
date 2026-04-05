/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_simple.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/17 10:25:18 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/03 10:46:00 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	check_pos(t_list *stack_b, int val)
{
	int		pos;
	t_list	*current;

	pos = 0;
	current = stack_b;
	while (current)
	{
		if (val > current->value)
			return (pos);
		pos++;
		current = current->next;
	}
	return (pos);
}

static void	to_b(t_list **stack_b, t_list **stack_a, t_options *opts)
{
	int	pos;
	int	i;

	pos = check_pos(*stack_b, (*stack_a)->value);
	i = pos;
	while (i > 0)
	{
		rotate_b(stack_b, opts->bench_mode, &opts->counters);
		i--;
	}
	push_b(stack_a, stack_b, opts->bench_mode, &opts->counters);
	i = pos;
	while (i > 0)
	{
		reverse_b(stack_b, opts->bench_mode, &opts->counters);
		i--;
	}
}

void	sort_simple(t_list **stack_a, t_list **stack_b, t_options *opts)
{
	while (*stack_a)
		to_b(stack_b, stack_a, opts);
	while (*stack_b)
		push_a(stack_b, stack_a, opts->bench_mode, &opts->counters);
}
