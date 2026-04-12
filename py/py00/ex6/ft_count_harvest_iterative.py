# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_count_harvest_iterative.py                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/02/27 02:32:02 by srasolov          #+#    #+#              #
#    Updated: 2026/02/27 10:14:38 by srasolov         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def ft_count_harvest_iterative():
    day = int(input("Days until harvest: "))
    for i in range(1 ,day + 1):
        print("Day ", i)
    print("Harvest time!")
