/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_swap.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/13 09:13:04 by srasolov          #+#    #+#             */
/*   Updated: 2025/10/14 10:39:28 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
//#include <stdio.h>

void	ft_swap(int *a, int *b)
{
	int	tmps;

	tmps = *a;
	*a = *b;
	*b = tmps;
}

/*int	main(void)
{
	int	x;
	int	y;

	x = 5;
	y = 9;
	printf("Avant\n");
	printf("x = %d || y = %d", x, y);
	ft_swap(&x, &y);
	printf("\nApres\n");
	printf("x = %d || y = %d", x, y);
}*/
