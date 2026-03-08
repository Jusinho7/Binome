/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/08 04:29:06 by srasolov          #+#    #+#             */
/*   Updated: 2026/03/08 16:11:25 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


#include "push_swap.h"

static int	word_count(const char *s, char c)
{
	int	count;
	int	in_word;

	count = 0;
	in_word = 0;
	while (*s)
	{
		if (*s != c && !in_word)
		{
			in_word = 1;
			count++;
		}
		else if (*s == c)
			in_word = 0;
		s++;
	}
	return (count);
}

static char	*word_dup(const char *start, int len)
{
	char	*word;
	int		i;

	word = malloc(len + 1);
	if (!word)
		return (0);
	i = 0;
	while (i < len)
	{
		word[i] = start[i];
		i++;
	}
	word[i] = '\0';
	return (word);
}

static int	ft_fill(char **str, const char *s, char c, int i)
{
	int	k;
	int	j;

	j = 0;
	while (s[i])
	{
		if (s[i] != c)
		{
			k = 0;
			while (s[i + k] && s[i + k] != c)
				k++;
			str[j++] = word_dup(s + i, k);
			i += k;
		}
		else
			i++;
	}
	str[j] = NULL;
	return (0);
}

char	**ft_split(char const *s, char c)
{
	char	**str;
	int		i;

	if (!s)
		return (0);
	str = malloc((word_count(s, c) + 1) * sizeof(char *));
	if (!str)
		return (0);
    i = 0;
	ft_fill(str, s, c, i);
	return (str);
}

void    ft_free_split(char **args)
{
    int i;

    if (!args)
        return ;
    i = 0;
    while (args[i])
    {
        free(args[i]);
        args[i] = NULL;
        i++;
    }
    free(args);
    args = NULL;
}
