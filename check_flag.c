/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   check_flag.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: frazanak <frazanak@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/16 11:04:53 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/11 20:00:55 by frazanak         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_algo	check_flag(char *arg)
{
	if (!arg)
		return (ADAPTIVE);
	if (ft_strcmp(arg, "--simple") == 0)
		return (SIMPLE);
	if (ft_strcmp(arg, "--medium") == 0)
		return (MEDIUM);
	if (ft_strcmp(arg, "--complex") == 0)
		return (COMPLEX);
	return (ADAPTIVE);
}

int	ft_lstsize(t_list *lst)
{
	int	count;

	count = 0;
	while (lst)
	{
		count++;
		lst = lst->next;
	}
	return (count);
}

int	check_disorder(t_list *stack)
{
	int		inversions;
	t_list	*i;
	t_list	*j;

	inversions = 0;
	i = stack;
	while (i)
	{
		j = i->next;
		while (j)
		{
			if (i->value > j->value)
				inversions++;
			j = j->next;
		}
		i = i->next;
	}
	return (inversions);
}

t_algo	detect_algo(t_list *stack)
{
	int		n;
	int		inv;
	int		max;
	double	disorder;

	n = ft_lstsize(stack);
	if (n <= 5)
		return (SIMPLE);
	inv = check_disorder(stack);
	max = (n * (n - 1)) / 2;
	disorder = (double)inv / (double)max;
	if (disorder < 0.2)
		return (SIMPLE);
	else if (disorder < 0.5)
		return (MEDIUM);
	else
		return (COMPLEX);
}

int	is_sorted(t_list *stack)
{
	t_list	*current;

	if (!stack || !stack->next)
		return (1);
	current = stack;
	while (current->next)
	{
		if (current->value > current->next->value)
			return (0);
		current = current->next;
	}
	return (1);
}
