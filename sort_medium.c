/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_medium.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: frazanak <frazanak@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/30 14:19:45 by frazanak          #+#    #+#             */
/*   Updated: 2026/04/08 12:46:25 by frazanak         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	get_chunk_size(t_list *stack_a)
{
	int	i;
	int	size_a;

	i = 0;
	size_a = ft_lstsize(stack_a);
	while (i * i < size_a)
		i++;
	return (i);
}

static void	rotate_ranks(int *ranks, int size_a)
{
	int	tmp;
	int	i;

	tmp = ranks[0];
	i = 0;
	while (i < size_a - 1)
	{
		ranks[i] = ranks[i + 1];
		i++;
	}
	ranks[size_a - 1] = tmp;
}

static void	to_b(t_list **stack_a, t_list **stack_b, t_chunk *chunk,
		t_options *opts)
{
	int	rotated;
	int	size_a;

	rotated = 0;
	size_a = ft_lstsize(*stack_a);
	while (*stack_a && rotated < size_a)
	{
		if (chunk->ranks[0] >= chunk->min && chunk->ranks[0] < chunk->max)
		{
			push_b(stack_a, stack_b, opts->bench_mode, &opts->counters);
			chunk->ranks++;
			size_a--;
		}
		else
		{
			rotate_a(stack_a, opts->bench_mode, &opts->counters);
			rotate_ranks(chunk->ranks, size_a);
			rotated++;
		}
	}
}

void	sort_medium(t_list **stack_a, t_list **stack_b, t_options *opts)
{
	int		*ranks;
	t_chunk	chunk;

	chunk.size = ft_lstsize(*stack_a);
	chunk.chunk_size = get_chunk_size(*stack_a);
	ranks = get_ranks(*stack_a, chunk.size);
	chunk.ranks = ranks;
	chunk.min = 0;
	chunk.max = chunk.min + chunk.chunk_size;
	while (chunk.min < chunk.size)
	{
		to_b(stack_a, stack_b, &chunk, opts);
		chunk.min += chunk.chunk_size;
		chunk.max = chunk.min + chunk.chunk_size;
	}
	free(ranks);
	while (*stack_b)
	{
		max_to_top_b(stack_b, opts);
		push_a(stack_b, stack_a, opts->bench_mode, &opts->counters);
	}
}
