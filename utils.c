/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/06 04:22:05 by srasolov          #+#    #+#             */
/*   Updated: 2026/03/27 19:45:25 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_list  *ft_new_node(int value)
{
    t_list  *new_node;

    new_node = (t_list *)malloc(sizeof(t_list));
    if (!new_node)
        return (0);
    new_node->value = value;
    new_node->next = NULL;
    return (new_node);
}

t_list *ft_lst_last(t_list *lst)
{
    if (!lst)
        return (0);
    while (lst->next)
        lst = lst->next;
    return (lst);
}

void	ft_lstadd_back(t_list **lst, t_list *new)
{
	t_list	*last;

	if (!new)
		return ;
	if (!(*lst))
	{
		*lst = new;
		return ;
	}
	last = ft_lst_last(*lst);
	last->next = new;
}

void    ft_error(t_list **stack)
{
    ft_free(stack);
    write(2, "Error\n", 6);
    exit (1);
}

void    ft_free(t_list **stack)
{
    t_list *tmp;

    while (*stack)
    {
        tmp = (*stack)->next;
        free(*stack);
        *stack = tmp;
    }    
}
