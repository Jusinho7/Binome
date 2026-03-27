/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   checker.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/08 03:59:29 by srasolov          #+#    #+#             */
/*   Updated: 2026/03/27 19:35:41 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void ft_check(t_list **stack_a, char **argv, int *num, int i)
{
	long    val;
	t_list  *node;

	if (!ft_isnumber(argv[i]))
		ft_error(stack_a);
	val = ft_atol(argv[i]);
	if (val > INT_MAX || val < INT_MIN)
		ft_error(stack_a);
	num[i] = (int)val;
	if (!check_doublon(num, i))
		ft_error(stack_a);
	node = ft_new_node((int)val);
	if (!node)
		ft_error(stack_a);
	ft_lstadd_back(stack_a, node);
}

void    ft_parse(t_list **stack_a, char **argv)
{
    int i;
    int size;
    int *num;

    size = count_arg(argv);
    num = malloc(sizeof(int) * size);
    if (!num)
        ft_error(stack_a);
    i = 0;
    while (argv[i])
    {
        ft_check(stack_a, argv, num, i);
        i++; 
    }
    free(num);
}

static int is_space(char c)
{
    if (c == 32 || (c >= 9 && c <= 13))
        return (1);
    return (0);
}

int is_blank(char *str)
{
    int i;

    if (!str || str[0] == '\0')
        return (1);
    i =  0;
    while (str[i])
    {
        if (!is_space(str[i]))
            return (0);
        i++;
    }
    return (1);
}
