/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_recursive_power.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/22 12:37:16 by srasolov          #+#    #+#             */
/*   Updated: 2025/10/22 13:12:58 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_recursive_power(int nb, int power)
{
	if (power < 0)
		return (0);
	else if (power == 0)
		return (1);
	else
		return (nb * ft_recursive_power(nb, power - 1));
	return (nb);
}

/*#include <stdio.h>

int	main(void)
{
	int	x;
	int	y;

	x = 5;
	y = 3;
	printf("%d", ft_recursive_power(x, y));
}*/
