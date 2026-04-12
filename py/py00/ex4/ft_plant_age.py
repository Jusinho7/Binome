# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_plant_age.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/31 08:42:02 by srasolov          #+#    #+#              #
#    Updated: 2026/03/31 08:44:52 by srasolov         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def ft_plant_age():
    age = int(input("Enter plant age in days: "))
    if age > 60:
        print("Plant is ready to harvest!")
    else:
        print("Plant needs more time to grow.")