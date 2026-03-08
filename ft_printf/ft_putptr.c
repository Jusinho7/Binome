/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putptr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/14 16:27:39 by srasolov          #+#    #+#             */
/*   Updated: 2026/02/14 16:36:47 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int ft_putptr(void *ptr)
{
    int i;
    char *str;

    if (!ptr)
        return (ft_putstr("0"));
        
    str = (unsigned char *)ptr;
    while (str[i])
    {
        ft_putchar(&str[i]);
        i++;
    }
    return (i);
}