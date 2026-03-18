/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/21 23:40:06 by srasolov          #+#    #+#             */
/*   Updated: 2026/03/03 00:29:10 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

static size_t	ft_strlen(const char *str)
{
	size_t	len;

	len = 0;
	if (!str)
		return (0);
	while (str[len])
		len++;
	return (len);
}

char	*ft_strchr(const char *str, int c)
{
	size_t	i;

	i = 0;
	if (!str)
		return (0);
	while (str[i])
	{
		if (str[i] == (char)c)
			return ((char *)&str[i]);
		i++;
	}
	if (c == '\0')
		return ((char *)str);
	return (0);
}

char	*ft_strdup(const char *str1)
{
	size_t	len;
	char	*str2;
	size_t	i;

	len = ft_strlen(str1);
	str2 = malloc(len + 1);
	i = 0;
	if (!str2)
		return (0);
	while (i < len)
	{
		str2[i] = str1[i];
		i++;
	}
	str2[i] = '\0';
	return (str2);
}

char	*ft_strjoin(char *str1, char *str2)
{
	size_t	i;
	size_t	j;
	char	*res;
	size_t	k;

	i = ft_strlen(str1);
	j = ft_strlen(str2);
	res = malloc(i + j + 1);
	k = 0;
	if (!res)
		return (0);
	while (k < i)
	{
		res[k] = str1[k];
		k++;
	}
	i = 0;
	while (i < j)
	{
		res[k] = str2[i];
		i++;
		k++;
	}
	res[k] = '\0';
	return (res);
}

char	*ft_new_line(char *content)
{
	size_t	i;
	size_t	j;
	size_t	len;
	char	*new;

	len = ft_strlen(content);
	i = 0;
	while (content[i] && content[i] != '\n')
		i++;
	if (!content[i])
	{
		free(content);
		return (0);
	}
	new = malloc(len - i + 1);
	if (!new)
		return (0);
	i++;
	j = 0;
	while (content[i])
		new[j++] = content[i++];
	new[j] = '\0';
	free(content);
	return (new);
}
