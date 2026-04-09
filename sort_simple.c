/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_simple.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/17 10:25:18 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/09 15:30:05 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	find_min(t_list *stack_a)
{
	int		min;
	t_list	*current;

	min = stack_a->value;
	current = stack_a;
	while (current)
	{
		if (current->value < min)
			min = current->value;
		current = current->next;
	}
	return (min);
}

static int	get_min_pos(t_list **stack_a, int min)
{
	t_list	*current;
	int		i;

	i = 0;
	current = *stack_a;
	while (current)
	{
		if (current->value == min)
			return (i);
		i++;
		current = current->next;
	}
	return (i);
}

static void	move_min_to_b(t_list **stack_a, t_list **stack_b, t_options *opts)
{
	int	min;
	int	pos;
	int	size;

	min = find_min(*stack_a);
	pos = get_min_pos(stack_a, min);
	size = ft_lstsize(*stack_a);
	if (pos <= size / 2)
		while (pos-- > 0)
			rotate_a(stack_a, opts->bench_mode, &opts->counters);
	else
		while (pos++ < size)
			reverse_a(stack_a, opts->bench_mode, &opts->counters);
	push_b(stack_a, stack_b, opts->bench_mode, &opts->counters);
}

void	sort_simple(t_list **stack_a, t_list **stack_, t_options *opts)
{
	int	size;

	size = ft_lstsize(*stack_a);
	while (size > 1)
	{
		move_min_to_b(stack_a, stack_, opts);
		size--;
	}
	while (*stack_)
		push_a(stack_, stack_a, opts->bench_mode, &opts->counters);
}
