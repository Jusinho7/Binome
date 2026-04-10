/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_simple.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: frazanak <frazanak@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/17 10:25:18 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/10 06:05:34 by frazanak         ###   ########.fr       */
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

static void	sort_three(t_list **stack_a, t_options *opts)
{
	int	a;
	int	b;
	int	c;

	a = (*stack_a)->value;
	b = (*stack_a)->next->value;
	c = (*stack_a)->next->next->value;
	if (a < c && c < b)
	{
		swap_a(stack_a, opts->bench_mode, &opts->counters);
		rotate_a(stack_a, opts->bench_mode, &opts->counters);
	}
	else if (b < a && a < c)
		swap_a(stack_a, opts->bench_mode, &opts->counters);
	else if (b < c && c < a)
		rotate_a(stack_a, opts->bench_mode, &opts->counters);
	else if (c < a && a < b)
		reverse_a(stack_a, opts->bench_mode, &opts->counters);
	else if (c < b && b < a)
	{
		rotate_a(stack_a, opts->bench_mode, &opts->counters);
		swap_a(stack_a, opts->bench_mode, &opts->counters);
	}
}

void	sort_simple(t_list **stack_a, t_list **stack_, t_options *opts)
{
	int	size;

	size = ft_lstsize(*stack_a);
	while (size > 3)
	{
		move_min_to_b(stack_a, stack_, opts);
		size--;
	}
	if (size == 3)
		sort_three(stack_a, opts);
	while (*stack_)
		push_a(stack_, stack_a, opts->bench_mode, &opts->counters);
}
