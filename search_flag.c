/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   search_flag.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/27 18:56:10 by srasolov          #+#    #+#             */
/*   Updated: 2026/03/27 19:52:43 by srasolov         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_algo  search_flag(int *argc, char **argv)
{
    t_algo  algo;
    t_algo  result;
    int i;

    algo = ADAPTIVE;
    i = 1;
    while (i < *argc)
    {
        result = check_flag(argv[i]);
        if (result != ADAPTIVE)
        {
            algo = result;
            while (i < *argc - 1)
            {
                argv[i] = argv[i + 1];
                i++;
            }
            argv[*argc - 1] = NULL;
            (*argc)--;
            break;
        }
        i++;
    }   
    return (algo);
}