/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_simple.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: frazanak <frazanak@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/17 10:25:18 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/04 20:21:09 by frazanak         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	find_min(t_list *stack)
{
	int		min;
	t_list	*curr;

	min = stack->value;
	curr = stack;
	while (curr)
	{
		if (curr->value < min)
			min = curr->value;
		curr = curr->next;
	}
	return (min);
}

static void	move_min_to_b(t_list **a, t_list **b)
{
	int	min;
	int	pos;
	int	size;
	int	i;
	t_list	*curr;

	min = find_min(*a);
	pos = 0;
	i = 0;
	curr = *a;
	while (curr)
	{
		if (curr->value == min)
			pos = i;
		i++;
		curr = curr->next;
	}
	size = ft_lstsize(*a);
	if (pos <= size / 2)
		while (pos-- > 0)
			rotate_a(a);
	else
		while (pos++ < size)
			reverse_a(a);
	push_b(a, b);
}

void	sort_simple(t_list **a, t_list **b)
{
	int	size;

	size = ft_lstsize(*a);
	while (size > 1)
	{
		move_min_to_b(a, b);
		size--;
	}
	while (*b)
		push_a(b, a);
}
