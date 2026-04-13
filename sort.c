/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/17 10:15:21 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/03 10:45:15 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	sort(t_list **stack_a, t_algo algo, t_algo *used_algo, t_options *opts)
{
	t_list	*stack_b;

	stack_b = NULL;
	if (is_sorted(*stack_a))
		return ;
	*used_algo = algo;
	if (algo == ADAPTIVE)
		*used_algo = detect_algo(*stack_a);
	if (*used_algo == SIMPLE)
		sort_simple(stack_a, &stack_b, opts);
	else if (*used_algo == MEDIUM)
		sort_medium(stack_a, &stack_b, opts);
	else if (*used_algo == COMPLEX)
		sort_complex(stack_a, &stack_b, opts);
}
