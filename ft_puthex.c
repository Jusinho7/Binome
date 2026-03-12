/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_puthex.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/17 22:19:10 by srasolov          #+#    #+#             */
/*   Updated: 2026/02/18 23:37:15 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_puthex(unsigned int num, char *base)
{
	int	count;

	count = 0;
	if (num >= 16)
		count += ft_puthex(num / 16, base);
	count += ft_putchar(base[num % 16]);
	return (count);
}
