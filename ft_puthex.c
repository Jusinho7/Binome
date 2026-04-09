/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_puthex.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/17 22:19:10 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/09 14:58:58 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_puthex_fd(unsigned int num, char *base, int fd)
{
	int	count;

	count = 0;
	if (num >= 16)
		count += ft_puthex_fd(num / 16, base, fd);
	count += ft_putchar_fd(base[num % 16], fd);
	return (count);
}
