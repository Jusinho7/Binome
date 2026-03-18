/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_str_is_alpha.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/15 08:39:35 by srasolov          #+#    #+#             */
/*   Updated: 2025/10/19 06:45:07 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
//#include <stdio.h>

int	ft_str_is_alpha(char *str)
{
	int	i;
	int	j;

	i = 0;
	while (str[i] != '\0')
	{
		j = str[i];
		if (!((j >= 'a' && j <= 'z') || (j >= 'A' && j <= 'Z')))
			return (0);
		i++;
	}
	return (1);
}

/*int	main(void)
{
	printf("%d", ft_str_is_alpha("Ss"));
	printf("\n%d\n", ft_str_is_alpha("Ecole42"));
	printf("%d\n", ft_str_is_alpha(""));
}*/
