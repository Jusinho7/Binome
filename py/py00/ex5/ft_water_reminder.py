# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_water_reminder.py                               :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/02/27 02:27:17 by srasolov          #+#    #+#              #
#    Updated: 2026/02/27 02:31:37 by srasolov         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def ft_water_reminder():
    day = int(input("Day since last watering: "))
    if day > 2:
        print("Water the plans!")
    else:
        print("Plants are fine")
