/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_simple.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/17 10:25:18 by srasolov          #+#    #+#             */
/*   Updated: 2026/03/17 13:48:46 by srasolov         ###   ########.fr       */
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

static void to_b(t_list **stack_b, int pos)
{
    int size;

    size = ft_lstsize(*stack_b);
    if (pos <= size / 2)
        while (pos > 0)
        {
            rotate_b(stack_b);
            pos--;
        }
    else
    {
        pos = size - pos;
        while (pos > 0)
        {
            reverse_b(stack_b);
            pos--;
        }   
    }
}

void    sort_simple(t_list **stack_a, t_list **stack_b)
{
    int pos;

    while (ft_lstsize(*stack_a) > 2)
    {
        pos = check_pos(*stack_b, (*stack_a)->value);
        to_b(stack_b, pos);
        push_b(stack_a, stack_b);
    }
    if ((*stack_a)->value > (*stack_a)->next->value)
        swap_a(stack_a);
    while (*stack_b)
        push_a(stack_b, stack_a);
}