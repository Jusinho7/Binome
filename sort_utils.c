/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_utils.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: frazanak <frazanak@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/30 14:19:45 by frazanak          #+#    #+#             */
/*   Updated: 2026/04/06 16:02:25 by frazanak         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	*get_ranks(t_list *stack_a, int size_a)
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
