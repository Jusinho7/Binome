# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_seed_inventory.py                               :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/02/27 02:46:57 by srasolov          #+#    #+#              #
#    Updated: 2026/03/31 08:52:24 by srasolov         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    packets = {
        "seed_type": seed_type,
        "quantity": quantity,
        "unit": unit
    }
    print(packets)    