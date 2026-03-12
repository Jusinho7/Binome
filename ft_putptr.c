/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putptr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/14 16:27:39 by srasolov          #+#    #+#             */
/*   Updated: 2026/02/18 23:38:46 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	ft_puthex_long(unsigned long num)
{
	int	count;

	count = 0;
	if (num >= 16)
		count += ft_puthex_long(num / 16);
	count += ft_putchar("0123456789abcdef"[num % 16]);
	return (count);
}

int	ft_putptr(void *ptr)
{
	int	count;

	if (!ptr)
		return (write(1, "(nil)", 5));
	count = 0;
	count += write(1, "0x", 2);
	count += ft_puthex_long((unsigned long)ptr);
	return (count);
}
