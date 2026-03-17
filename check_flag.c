/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   check_flag.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/16 11:04:53 by srasolov          #+#    #+#             */
/*   Updated: 2026/03/17 10:07:55 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_algo  check_flag(char *arg)
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

int check_disorder(t_list *stack)
{
    int     inversions;
    t_list  *i;
    t_list  *j;

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

t_algo  detect_algo(t_list *stack)
{
    int n;
    int inv;
    int max;

    n = ft_lstsize(stack);
    inv = check_disorder(stack);
    max = (n * (n - 1)) / 2;  
    if (inv < max * 0.1)       
        return (SIMPLE);
    else if (inv < max * 0.5)  
        return (MEDIUM);
    else
        return (COMPLEX);
}
