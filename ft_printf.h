/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/14 16:13:32 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/03 11:51:14 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include <stdarg.h>
# include <unistd.h>

int	ft_printf_fd(int fd, const char *format, ...);
int	set_format_fd_branch2(char set_type, va_list args, int fd);
int	ft_putunsigned_fd(unsigned int num, int fd);
int	ft_puthex_fd(unsigned int num, char *base, int fd);
int	ft_putchar_fd(int c, int fd);
int	ft_putstr_fd(char *str, int fd);
int	ft_puthex_long_fd(unsigned long num, int fd);
int	ft_putptr_fd(void *ptr, int fd);
int	ft_putnbr_fd(long num, int fd);

#endif
