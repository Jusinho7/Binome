/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_complex.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: frazanak <frazanak@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/01 19:57:26 by frazanak          #+#    #+#             */
/*   Updated: 2026/04/01 19:57:26 by frazanak         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	get_max_bits(int max_rank)
{
	int	bits;

	bits = 0;
	while ((max_rank >> bits) != 0)
		bits++;
	return (bits);
}

static void	replace_with_ranks(t_list *stack_a, int *ranks)
{
	int		i;
	t_list	*current;

	i = 0;
	current = stack_a;
	while (current)
	{
		current->value = ranks[i++];
		current = current->next;
	}
}

static void	process_one_bit(t_list **a, t_list **b, int bit, int size_a)
{
	int	i;

	i = 0;
	while (i < size_a)
	{
		if ((((*a)->value >> bit) & 1) == 0)
			push_b(a, b);
		else
			rotate_a(a);
		i++;
	}
}

static void	sort_by_bits(t_list **a, t_list **b, int bits, int size_a)
{
	int	bit;

	bit = 0;
	while (bit < bits)
	{
		process_one_bit(a, b, bit, size_a);
		while (*b)
			push_a(b, a);
		bit++;
	}
}

void	sort_complex(t_list **stack_a, t_list **stack_b)
{
	int		size_a;
	int		*originals;
	int		bits;

	size_a = ft_lstsize(*stack_a);
	originals = save_originals(*stack_a, size_a);
	if (!originals)
		return ;
	replace_with_ranks(*stack_a, get_ranks(*stack_a, size_a));
	bits = get_max_bits(get_max_value(*stack_a));
	sort_by_bits(stack_a, stack_b, bits, size_a);
	restore_values(*stack_a, originals);
	free(originals);
}
