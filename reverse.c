/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   reverse.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/05 02:42:13 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/03 11:40:44 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	ft_reverse(t_list **stack)
{
	t_list	*temps;
	t_list	*last;

	if (!(*stack) || !(*stack)->next)
		return ;
	temps = *stack;
	last = ft_lst_last(*stack);
	while (temps->next != last)
		temps = temps->next;
	temps->next = NULL;
	last->next = *stack;
	*stack = last;
}

void	reverse_a(t_list **stack_a, int bench_mode, t_counters *counters)
{
	ft_reverse(stack_a);
	write(1, "rra\n", 4);
	if (bench_mode)
		counters->rra++;
}

void	reverse_b(t_list **stack_b, int bench_mode, t_counters *counters)
{
	ft_reverse(stack_b);
	write(1, "rrb\n", 4);
	if (bench_mode)
		counters->rrb++;
}

void	reverse_all(t_list **stack_a, t_list **stack_b, int bench_mode,
		t_counters *counters)
{
	ft_reverse(stack_a);
	ft_reverse(stack_b);
	write(1, "rrr\n", 4);
	if (bench_mode)
		counters->rrr++;
}
