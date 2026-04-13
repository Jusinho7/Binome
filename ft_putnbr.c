/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/14 16:23:10 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/03 11:53:29 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putnbr(int num)
{
	int		count;
	long	nbr;

	count = 0;
	nbr = num;
	if (nbr < 0)
	{
		count += ft_putchar('-');
		nbr = -nbr;
	}
	if (nbr >= 10)
		count += ft_putnbr(nbr / 10);
	count += ft_putchar(nbr % 10 + '0');
	return (count);
}

int	ft_putnbr_fd(long num, int fd)
{
	int	count;

	count = 0;
	if (num < 0)
	{
		count += ft_putchar_fd('-', fd);
		num = -num;
	}
	if (num >= 10)
		count += ft_putnbr_fd(num / 10, fd);
	count += ft_putchar_fd((num % 10) + '0', fd);
	return (count);
}
