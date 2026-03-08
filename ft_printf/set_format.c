/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   set_format.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/14 16:19:09 by srasolov          #+#    #+#             */
/*   Updated: 2026/02/14 16:19:39 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	set_format(char set_type, va_list args)
{
	if (set_type == 'c')
		return (ft_putchar(va_arg(args, int)));
	else if (set_type == 's')
		return (ft_putstr(va_arg(args, char *)));
	else if (set_type == 'p')
		return (ft_putptr(va_arg(args, void *)));
	else if (set_type == 'd' || set_type == 'i')
		return (ft_putnbr(va_arg(args, int)));
	else if (set_type == 'u')
		return (ft_putunsigned(va_arg(args, unsigned int)));
	else if (set_type == 'x')
		return (ft_puthex(va_arg(args, unsigned int), "0123456789abcdef"));
	else if (set_type == 'X')
		return (ft_puthex(va_arg(args, unsigned int), "0123456789ABCDEF"));
	else if (set_type == '%')
		return (write(1, "%", 1));
	return (0);
}