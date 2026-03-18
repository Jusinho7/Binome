/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_sort_int_tab.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/14 09:42:46 by srasolov          #+#    #+#             */
/*   Updated: 2025/10/14 10:55:58 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
//#include <stdio.h>

void	ft_sort_int_tab(int *tab, int size)
{
	int	i;
	int	j;
	int	min;
	int	temps;

	i = 0;
	while (i < size -1)
	{
		min = i;
		j = i + 1;
		while (j < size)
		{
			if (tab[j] < tab[min])
				min = j;
			j++;
		}
		temps = tab[i];
		tab[i] = tab[min];
		tab[min] = temps;
		i++;
	}
}

/*int	main(void)
{
	int	tab[9] = {9, 5, 4, 6, 8, 7, 1, 2, 5};
	int	size = 9;
	int	i;

	ft_sort_int_tab(tab, size);
	i = 0;
	while (i < size)
	{
		printf("%d, ", tab[i]);
		i++;
	}
}*/
