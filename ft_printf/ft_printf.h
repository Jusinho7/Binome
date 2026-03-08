/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/14 16:13:32 by srasolov          #+#    #+#             */
/*   Updated: 2026/02/14 16:20:23 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include <stdarg.h>
# include <unistd.h>

int ft_printf(const char *format, ...);
int set_format(char set_type, va_list args);
int ft_putchar(int c);
int ft_putstr(char *str);
int ft_putptr(void *ptr);
int ft_putnbr(int n);
int ft_putunsigned(unsigned int n);
int ft_puthex(unsigned int n, char *base);

#endif
