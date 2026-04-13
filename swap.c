/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   swap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/04 02:06:13 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/03 11:39:58 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	ft_swap(t_list **stack)
{
	t_list	*temps;

	if (!(*stack) || !(*stack)->next)
		return ;
	temps = *stack;
	*stack = (*stack)->next;
	temps->next = (*stack)->next;
	(*stack)->next = temps;
}

void	swap_a(t_list **stack_a, int bench_mode, t_counters *counters)
{
	ft_swap(stack_a);
	write(1, "sa\n", 3);
	if (bench_mode)
		counters->sa++;
}

void	swap_b(t_list **stack_b, int bench_mode, t_counters *counters)
{
	ft_swap(stack_b);
	write(1, "sb\n", 3);
	if (bench_mode)
		counters->sb++;
}

void	swap_all(t_list **stack_a, t_list **stack_b, int bench_mode,
		t_counters *counters)
{
	ft_swap(stack_a);
	ft_swap(stack_b);
	write(1, "ss\n", 3);
	if (bench_mode)
		counters->ss++;
}
