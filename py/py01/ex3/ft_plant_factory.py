# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_plant_factory.py                                :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/31 21:35:51 by srasolov          #+#    #+#              #
#    Updated: 2026/04/12 07:43:59 by srasolov         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class Plant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self.name = name
        self.height_init = height 
        self.age_init = age

    def show(self):
        print(f"Created: {self.name}: {self.height_init} cm {self.age_init} days old")

def main():
    print("===  Plant Factory Output ==")
    
    plants = [
        Plant("Rose", 25.0, 30),
        Plant("Oak", 200.0, 365),
        Plant("Cactus", 5.0, 90),
        Plant("Sunflower", 80.0, 45),
        Plant("Fern", 15.0, 120),
    ]

    for i in plants:
        i.show()

if __name__ == "__main__":
    main()

    