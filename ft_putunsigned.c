/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putunsigned.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/17 22:13:33 by srasolov          #+#    #+#             */
/*   Updated: 2026/02/18 23:39:43 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putunsigned(unsigned int num)
{
	int	count;

	count = 0;
	if (num >= 10)
		count += ft_putunsigned(num / 10);
	count += ft_putchar(num % 10 + '0');
	return (count);
}
