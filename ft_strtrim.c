/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/29 13:22:23 by srasolov          #+#    #+#             */
/*   Updated: 2026/02/01 07:02:26 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	is_set(char c, const char *s)
{
	size_t	i;

	i = 0;
	while (s[i])
	{
		if (s[i] == c)
			return (1);
		i++;
	}
	return (0);
}

char	*ft_strtrim(char const *s1, char const *set)
{
	size_t	i;
	size_t	j;
	size_t	len;
	char	*str;

	if (!s1 || !set)
		return (0);
	j = ft_strlen(s1) - 1;
	i = 0;
	while (s1[i] && is_set(s1[i], set))
		i++;
	while (j >= i && is_set(s1[j], set))
		j--;
	len = j - i + 1;
	str = malloc (len + 1);
	if (!str)
		return (0);
	ft_memcpy(str, &s1[i], len);
	str[len] = '\0';
	return (str);
}
