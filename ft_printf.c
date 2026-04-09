/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/14 15:33:36 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/09 14:58:20 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	handle_float_fd(double val, int fd)
{
	int	whole;
	int	fract;
	int	count;

	whole = (int)val;
	fract = (int)((val - whole) * 100 + 0.5);
	if (fract >= 100)
	{
		whole++;
		fract = 0;
	}
	count = 0;
	count += ft_putnbr_fd(whole, fd);
	count += ft_putchar_fd('.', fd);
	if (fract < 10)
		count += ft_putchar_fd('0', fd);
	count += ft_putnbr_fd(fract, fd);
	return (count);
}

static int	set_format_fd(char set_type, va_list args, int fd)
{
	if (set_type == 'c')
		return (ft_putchar_fd(va_arg(args, int), fd));
	else if (set_type == 's')
		return (ft_putstr_fd(va_arg(args, char *), fd));
	else if (set_type == 'p')
		return (ft_putptr_fd(va_arg(args, void *), fd));
	else if (set_type == 'd' || set_type == 'i')
		return (ft_putnbr_fd(va_arg(args, int), fd));
	else if (set_type == 'u')
		return (ft_putunsigned_fd(va_arg(args, unsigned int), fd));
	else if (set_type == 'x')
		return (ft_puthex_fd(va_arg(args, unsigned int), "0123456789abcdef",
				fd));
	else if (set_type == 'X')
		return (ft_puthex_fd(va_arg(args, unsigned int), "0123456789ABCDEF",
				fd));
	else if (set_type == 'f')
		return (handle_float_fd(va_arg(args, double), fd));
	else if (set_type == '%')
		return (write(fd, "%", 1));
	return (0);
}

int	ft_printf_fd(int fd, const char *format, ...)
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
			count += set_format_fd(format[i], args, fd);
		}
		else if (format[i] != '%')
			count += ft_putchar_fd(format[i], fd);
		i++;
	}
	va_end(args);
	return (count);
}
