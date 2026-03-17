/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/17 10:15:21 by srasolov          #+#    #+#             */
/*   Updated: 2026/03/17 10:15:59 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void    sort(t_list **stack_a, t_algo algo)
{
    t_list  *stack_b;

    stack_b = NULL;
    if (algo == ADAPTIVE)
        algo = detect_algo(*stack_a);
    if (algo == SIMPLE)
        sort_simple(stack_a, &stack_b);
    else if (algo == MEDIUM)
        sort_medium(stack_a, &stack_b);
    else if (algo == COMPLEX)
        sort_complex(stack_a, &stack_b);
}