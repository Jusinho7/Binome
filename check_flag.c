/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   check_flag.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/16 11:04:53 by srasolov          #+#    #+#             */
/*   Updated: 2026/03/16 11:05:03 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_algo  check_flag(char *arg)
{
    if (!arg)
        return (ADAPTIVE);
    if (ft_strcmp(arg, "--simple") == 0)
        return (SIMPLE);
    if (ft_strcmp(arg, "--medium") == 0)
        return (MEDIUM);
    if (ft_strcmp(arg, "--complex") == 0)
        return (COMPLEX);
    return (ADAPTIVE); 
}
