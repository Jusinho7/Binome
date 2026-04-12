# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_count_harvest_recursive.py                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/02/27 02:32:02 by srasolov          #+#    #+#              #
#    Updated: 2026/02/27 10:18:26 by srasolov         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def helper(day, i = 1):
    if i > day:
        print("Harvest time!")
        return
    print("Day ", i)
    helper(day, i + 1)

def ft_count_harvest_recursive():
    day = int(input("Days until harvest: "))
    helper(day)

    
