/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   check_files.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/06 10:39:09 by srasolov          #+#    #+#             */
/*   Updated: 2026/03/06 11:19:25 by srasolov         ###   ########.fr       */
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
    int j;

    i = 0;
    while (i < len)
    {
        j = i + 1;
        while (j < len)
        {
            if (num[i] == num[j])
                return (1);
            j++;
        }
        i++;
    }
    return (0);
}

