/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_rev_int_tab.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/14 08:12:29 by srasolov          #+#    #+#             */
/*   Updated: 2025/10/14 10:53:51 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
//#include <stdio.h>

void	ft_rev_int_tab(int *tab, int size)
{
	int	temps;
	int	i;

	i = 0;
	while (i < size / 2)
	{
		temps = tab[i];
		tab[i] = tab[(size - i) - 1];
		tab[(size - i) - 1] = temps;
		i++;
	}
}

/*int	main(void)
{
	int	tab[9] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
	int	size = 9;

	int	i;
	ft_rev_int_tab(tab, size);

	i = 0;
	while (i < size)
	{
		printf("%d", tab[i]);
		i++;
	}
}*/
