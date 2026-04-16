/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putunsigned.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/17 22:13:33 by srasolov          #+#    #+#             */
/*   Updated: 2026/04/03 11:53:50 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putunsigned_fd(unsigned int num, int fd)
{
	int	count;

	count = 0;
	if (num >= 10)
		count += ft_putunsigned_fd(num / 10, fd);
	count += ft_putchar_fd((num % 10) + '0', fd);
	return (count);
}
