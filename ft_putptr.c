/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putptr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/14 16:27:39 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/03 11:53:20 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_puthex_long_fd(unsigned long num, int fd)
{
	int	count;

	count = 0;
	if (num >= 16)
		count += ft_puthex_long_fd(num / 16, fd);
	count += ft_putchar_fd("0123456789abcdef"[num % 16], fd);
	return (count);
}

int	ft_putptr_fd(void *ptr, int fd)
{
	int	count;

	if (!ptr)
		return (write(fd, "(nil)", 5));
	count = 0;
	count += write(fd, "0x", 2);
	count += ft_puthex_long_fd((unsigned long)ptr, fd);
	return (count);
}
