/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/04 03:46:13 by srasolov          #+#    #+#             */
/*   Updated: 2026/03/06 07:05:08 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void ft_push(t_list **stack_a, t_list **stack_b)
{
    t_list  *temps;

    if (!*stack_a)
        return ;
    temps = *stack_a;
    *stack_a = (*stack_a)->next;
    temps->next = *stack_b;
    *stack_b = temps;
}

void    push_a(t_list **stack_b, t_list **stack_a)
{
    ft_push(stack_b, stack_a);
    write(1, "pa\n", 3);
}

void    push_b(t_list **stack_a, t_list **stack_b)
{
    ft_push(stack_a, stack_b);
    write(1, "pb\n", 3);
}

