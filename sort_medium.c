/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_medium.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/30 14:19:45 by frazanak          #+#    #+#             */
/*   Updated: 2026/04/05 12:02:55 by srasolov         ###   ########.fr       */
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

static int	*get_ranks(t_list *stack_a, int size_a)
{
	int		*ranks;
	int		i;
	t_list	*current;
	int		rank;
	t_list	*tmp;

	ranks = malloc(size_a * sizeof(int));
	if (!ranks)
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
	int		size_a;
	int		*ranks;
	t_chunk	chunk;

	size_a = ft_lstsize(*stack_a);
	chunk.chunk_size = get_chunk_size(*stack_a);
	ranks = get_ranks(*stack_a, size_a);
	chunk.ranks = ranks;
	chunk.min = 0;
	chunk.max = chunk.min + chunk.chunk_size;
	chunk.size = size_a;
	while (chunk.min < size_a)
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
