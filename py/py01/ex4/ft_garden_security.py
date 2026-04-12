# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_garden_security.py                              :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: srasolov <srasolov@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/04/01 04:19:36 by srasolov          #+#    #+#              #
#    Updated: 2026/04/12 07:45:43 by srasolov         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class Plant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self._name = name

        if height < 0:
            print("Height update rejected")
            self._height = 0
        else:
            self._height = height
        if age < 0:
            print("Age update rejected")
            self._age = 0
        else:
            self._age = age
        
    def get_height(self):
        return self._height

    def get_age(self):
        return self._age
        
    def set_height(self, height):
        if height < 0:
            print(f"{self._name}: Error, height can't be negative")
            print("Height update rejected")
        else:
            self._height = height
            print(f"Height updated: {self._height}cm")
        
    def set_age(self, age):
        if age < 0:
            print(f"{self._name}: Error, age can't be negative")
            print("Age update rejected")
        else:
            self._age = age
            print(f"Age updated: {self._age} days\n")
            
    def show(self):
        return f"{self._name}: {self._height}cm, {self._age} days old"

def main():
    print("=== Garden Security System ===")

    rose = Plant("Rose", 15.0, 10)
    print(f"Plant created: {rose.show()}\n")
    rose.set_height(25)
    rose.set_age(30)
    rose.set_height(-5)
    rose.set_age(-2)
    print(f"\nCurrent state: {rose.show()}")

if __name__ == "__main__":
    main()
