# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_plant_growth.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/31 13:44:23 by srasolov          #+#    #+#              #
#    Updated: 2026/04/01 04:05:00 by srasolov         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class Plant:
    def __init__(self):
        self.name = None
        self.height = None
        self.age = None
        self.growth_rate = None

    def show(self):
        print(f"{self.name}: {self.height} cm {self.age} days old")
        
    def grow(self):
        self.height = round(self.height + self.growth_rate, 1)

    def few_age(self):
        self.age += 1
        

def main():
    print("=== Garden Plant Growth ===")
        
    rose = Plant()
    rose.name = "Rose"
    rose.height = 25.0
    rose.age = 30
    rose.growth_rate = 0.8
    
    height_init = rose.height
    
    for day in range(1, 8):
        rose.grow()
        rose.few_age()
        print("\n=== Day", str(day), "===")
        rose.show()

    total_height = rose.height - height_init
    print(f"\nGrowth this week: {int(round(total_height, 0))} cm")    
    
if __name__== "__main__":
    main()

