/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/14 15:33:36 by srasolov          #+#    #+#             */
/*   Updated: 2026/03/10 20:10:04 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	set_format(char set_type, va_list args)
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

int	ft_printf(const char *format, ...)
{
	va_list	args;
	int		count;
	int		i;

	i = 0;
	count = 0;
	va_start(args, format);
	while (format[i])
	{
		if (format[i] == '%' && format[i + 1])
		{
			i++;
			count += set_format(format[i], args);
		}
		else if (format[i] != '%')
			count += ft_putchar(format[i]);
		i++;
	}
	va_end(args);
	return (count);
}
