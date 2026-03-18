/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnstr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/29 12:33:42 by srasolov          #+#    #+#             */
/*   Updated: 2026/01/29 12:41:24 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strnstr(const char *big, const char *tittle, size_t len)
{
	size_t	i;
	size_t	j;

	if (*tittle == '\0')
		return ((char *)big);
	i = 0;
	while (big[i] && i < len)
	{
		j = 0;
		while (big[i + j]
			&& tittle[j]
			&& i + j < len
			&& big[i + j] == tittle[j])
			j++;
		if (tittle[j] == '\0')
			return ((char *)&big[i]);
		i++;
	}
	return (0);
}
