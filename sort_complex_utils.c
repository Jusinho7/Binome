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

int	*save_originals(t_list *stack, int size)
{
	int		*originals;
	int		*ranks;
	int		i;
	t_list	*curr;

	ranks = get_ranks(stack, size);
	if (!ranks)
		return (NULL);
	originals = malloc(sizeof(int) * size);
	if (!originals)
	{
		free(ranks);
		return (NULL);
	}
	i = 0;
	curr = stack;
	while (curr)
	{
		originals[ranks[i++]] = curr->value;
		curr = curr->next;
	}
	free(ranks);
	return (originals);
}

void	restore_values(t_list *stack, int *originals)
{
	t_list	*curr;
	int		i;

	curr = stack;
	i = 0;
	while (curr)
	{
		curr->value = originals[i++];
		curr = curr->next;
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
