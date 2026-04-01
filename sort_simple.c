/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_simple.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: frazanak <frazanak@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/17 10:25:18 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/01 14:54:41 by frazanak         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int  check_pos(t_list *stack_b, int val)
{
    int     pos;
    t_list  *current;

    pos = 0;
    current = stack_b;
    while (current)
    {
        if (val > current->value)
            return (pos);
        pos++;
        current = current->next;
    }
    return (pos);
}

static void to_b(t_list **stack_b, t_list **stack_a)
{
    int pos;
    int i;

    pos = check_pos(*stack_b, (*stack_a)->value);
    i = pos;
    while (i > 0)
    {
        rotate_b(stack_b);
        i--;
    }
    push_b(stack_a, stack_b);
    i = pos;
    while (i > 0)
    {
        reverse_b(stack_b);
        i--;
    }
}

void    sort_simple(t_list **stack_a, t_list **stack_b)
{
    while (*stack_a)
        to_b(stack_b, stack_a);
    while (*stack_b)
        push_a(stack_b, stack_a);
}
