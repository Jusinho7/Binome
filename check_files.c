/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   check_files.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/06 10:39:09 by srasolov          #+#    #+#             */
/*   Updated: 2026/03/27 19:45:22 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

long	ft_atol(const char *nptr)
{
	long	result;
	int	sign;
	int	i;

	i = 0;
	sign = 1;
	result = 0;
	if (!nptr)
		return (0);
	while (nptr[i] == 32 || (nptr[i] >= 9 && nptr[i] <= 13))
		i++;
	if (nptr[i] == '-' || nptr[i] == '+')
	{
		if (nptr[i] == '-')
			sign *= -1;
		i++;
	}
	while (nptr[i] >= '0' && nptr[i] <= '9')
	{
		result = (result * 10) + (nptr[i] - '0');
        if (result * sign > (long)INT_MAX || result * sign < (long)INT_MIN)
            return (result * sign);
		i++;
	}
	return (result * sign);
}

int check_doublon(int *num, int len)
{
    int i;

    i = 0;
    while (i < len)
    {
        if (num[i] == num[len])
            return (0);
        i++;
    }
    return (1);
}

void    ft_print(t_list *stack, char *name)
{
    int i;

    i = 0;
    ft_printf("Stack %s: ", name);
    while (stack)
    {
        ft_printf("[%d]", stack->value);
        stack = stack->next;
        i++;
    }
    ft_printf("\n");
}

int	count_arg(char **args)
{
	int	len;

	len = 0;
	while (args[len])
		len++;
	return (len);
}

int	ft_isnumber(char *str)
{
	int	i;

	i = 0;	
	while (str[i] == 32 || (str[i] >= 9 && str[i] <= 13))
		i++;
	if (str[i] == '-' || str[i] == '+')
		i++;
	if (!str[i])
		return (0);
	while (str[i])
	{
		if (str[i] < '0' || str[i] > '9')
			return (0);
		i++;
	}
	return (1);
}
