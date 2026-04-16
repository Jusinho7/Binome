/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils2.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/16 06:34:19 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/16 07:18:29 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

char	*ft_strcat(char *dest, char *src)
{
	int	i;
	int	j;

	i = 0;
	while (dest[i] != '\0')
		i++;
	j = 0;
	while (src[j] != '\0')
	{
		dest[i] = src[j];
		i++;
		j++;
	}
	dest[i] = '\0';
	return (dest);
}

int	ft_strlen(char *str)
{
	int	count;

	count = 0;
	while (str[count] != '\0')
		count++;
	return (count);
}

int	calc_joined_len(int argc, char **argv, int *valid_args)
{
	int	total_len;
	int	i;

	total_len = 0;
	*valid_args = 0;
	i = 1;
	while (i < argc)
	{
		if (argv[i] && !is_blank(argv[i]))
		{
			total_len += ft_strlen(argv[i]) + 1;
			(*valid_args)++;
		}
		i++;
	}
	return (total_len);
}

char	*build_joined(int argc, char **argv, t_list **stack_a)
{
	char	*joined;
	int		total_len;
	int		valid_args;
	int		i;

	total_len = calc_joined_len(argc, argv, &valid_args);
	if (valid_args == 0)
		ft_error(stack_a);
	joined = malloc(total_len + 1);
	if (!joined)
		ft_error(stack_a);
	*joined = '\0';
	i = 0;
	while (++i < argc)
	{
		if (argv[i] && !is_blank(argv[i]))
		{
			if (*joined)
				ft_strcat(joined, " ");
			ft_strcat(joined, argv[i]);
		}
	}
	return (joined);
}
