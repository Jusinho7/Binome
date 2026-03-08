/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/03 19:29:12 by srasolov          #+#    #+#             */
/*   Updated: 2026/03/08 07:35:14 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSHSWAP_H
# define PUSHSWAP_H

# include <unistd.h>
# include <stdlib.h>
# include <limits.h>
#include <stdio.h>

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

void    ft_parse(t_list **stack_a, char **argv);
int check_doublon(int *num, int len);
long	ft_atol(const char *nptr);
int	count_arg(char **args);
char	**ft_split(char const *s, char c);
void    ft_free_split(char **args);
int	ft_isdigit(char *str);
int is_blank(char *str);

void    ft_error(t_list **stack);
void    ft_free(t_list **stack);

void    ft_print(t_list *stack, char *name);

#endif
