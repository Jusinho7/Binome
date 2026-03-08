/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rotate.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/05 01:51:34 by srasolov          #+#    #+#             */
/*   Updated: 2026/03/06 07:04:56 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void ft_rotate(t_list **stack)
{
    t_list  *temps;
    t_list  *last;

    if (!(*stack) || !(*stack)->next)
        return ;
    temps = *stack;
    *stack = temps->next;
    last = ft_lst_last(*stack);
    last->next = temps;
    temps->next = NULL;
}

void    rotate_a(t_list **stack_a)
{
    ft_rotate(stack_a);
    write(1, "ra\n", 3);
}

void    rotate_b(t_list **stack_b)
{
    ft_rotate(stack_b);
    write(1, "rb\n", 3);
}

void    rotate_all(t_list **stack_a, t_list **stack_b)
{
    ft_rotate(stack_a);
    ft_rotate(stack_b);
    write(1, "rr\n", 3);
}

