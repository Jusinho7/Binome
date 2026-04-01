/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_medium.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: frazanak <frazanak@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/30 14:19:45 by frazanak          #+#    #+#             */
/*   Updated: 2026/03/30 14:19:45 by frazanak         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	get_chunck_size(t_list *stack_a)
{
	int	i;
	int	size;

	i = 0;
	size = ft_lstsize(stack_a);
	while (i * i < size)
		i++;
	return (i);
}

static int*	get_ranks(t_list *stack_a, int size)
{
    int     *ranks;
    int     i;
    t_list  *current;
    int     rank;
    t_list  *tmp;

	ranks = malloc(size * sizeof(int));
	if(!ranks)
		return (NULL);
	i = 0;
	current = stack_a;
	while (current)
	{
		rank = 0;
		tmp = stack_a;
		while (tmp)
		{	
			if (current->value > tmp->value)
				rank++;
			tmp = tmp->next;
		}
		ranks[i++] = rank;
		current = current->next;
	}
	return (ranks);
}

static void	to_b(t_list **stack_a, t_list **stack_b, int min, int max)
{
	int	*ranks;
	int	size;
	int	rotated;

	rotated = 0;
	size = ft_lstsize(*stack_a);
	while (rotated < size)
	{
		ranks = get_ranks(*stack_a, ft_lstsize(*stack_a));
		if (!ranks)
			return ;
		if (ranks[0] >= min && ranks[0] < max)
		{
			push_b(stack_a, stack_b);
			free(ranks);
		}
		else
		{
			rotate_a(stack_a);
			free(ranks);
			rotated++;
		}
	}
}

void	sort_medium(t_list **stack_a, t_list **stack_b)
{
	int	chunk_size;
	int	size;
	int	min;

	chunk_size = get_chunck_size(*stack_a);
	size = ft_lstsize(*stack_a);
	min = 0;
	while (min < size)
	{
		to_b(stack_a, stack_b, min, min + chunk_size);
		min += chunk_size;
	}
	while (*stack_b)
	{
		max_to_top_b(stack_b);
		push_a(stack_b, stack_a);
	}
}