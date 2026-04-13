/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/04 03:46:13 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/03 10:03:39 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	ft_push(t_list **stack_a, t_list **stack_b)
{
	t_list	*temps;

	if (!*stack_a)
		return ;
	temps = *stack_a;
	*stack_a = (*stack_a)->next;
	temps->next = *stack_b;
	*stack_b = temps;
}

void	push_a(t_list **stack_b, t_list **stack_a, int bench_mode,
		t_counters *counters)
{
	ft_push(stack_b, stack_a);
	write(1, "pa\n", 3);
	if (bench_mode)
		counters->pa++;
}

void	push_b(t_list **stack_a, t_list **stack_b, int bench_mode,
		t_counters *counters)
{
	ft_push(stack_a, stack_b);
	write(1, "pb\n", 3);
	if (bench_mode)
		counters->pb++;
}
