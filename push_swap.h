/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/03 19:29:12 by srasolov          #+#    #+#             */
/*   Updated: 2026/03/06 11:25:07 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSHSWAP_H
# define PUSHSWAP_H

# include <unistd.h>
# include <stdlib.h>
# include <limits.h>

typedef struct  s_list
{
    int value;
    struct s_list  *next;
}   t_list;

t_list *ft_lst_last(t_list *lst);
void    reverse_a(t_list **stack_a);
void    reverse_b(t_list **stack_b);
void    reverse_all(t_list **stack_a, t_list **stack_b);
void    rotate_a(t_list **stack_a);
void    rotate_b(t_list **stack_b);
void    rotate_all(t_list **stack_a, t_list **stack_b);
void    swap_a(t_list **stack_a);
void    swap_b(t_list **stack_b);
void    swap_all(t_list **stack_a, t_list **stack_b);
void    push_a(t_list **stack_b, t_list **stack_a);
void    push_b(t_list **stack_a, t_list **stack_b);
t_list  *ft_new_node(int value);
void	ft_lstadd_back(t_list **lst, t_list *new);

int check_doublon(int *num, int len);
long	ft_atol(const char *nptr);

#endif
