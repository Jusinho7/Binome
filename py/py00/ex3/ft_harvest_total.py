# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_harvest_total.py                                :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/02/27 02:07:33 by srasolov          #+#    #+#              #
#    Updated: 2026/02/27 02:22:40 by srasolov         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def ft_harvest_total():
    total = 0
    i = 1
    while (i <= 3):
        day = int(input("Day " + str(i) + " harvest: "))
        i += 1
        total += day  
    print("Total harvest: ", total)

