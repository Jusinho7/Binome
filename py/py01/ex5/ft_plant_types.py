class Plant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self._name = name
        self._height = height
        self._age = age

    def show(self):
        print(f"{self._name}: {self._height}cm, {self._age} days old")

    def grow(self, growth_rate):
        self._height = round(self._height + growth_rate, 1)

    def few_age(self):
        self._age += 1


class Flower(Plant):
    def __init__(self, name: str, height: int, age: int, color: str) -> None:
        super().__init__(name, height, age)
        self._color = color
        self._to_bloom = False

    def show(self):
        super().show()
        print(f"Color: {self._color}")
        if self._to_bloom:
            print(f"{self._name} is blooming beautifully!")
        else:
            print(f"{self._name} has not bloomed yet")

    def bloom(self):
        self._to_bloom = True


class Tree(Plant):
    def __init__(
        self,
        name: str,
        height: int,
        age: int,
        trunk_diameter: int,
    ) -> None:
        super().__init__(name, height, age)
        self._trunk_diameter = trunk_diameter

    def show(self):
        super().show()
        print(f"Trunk diameter:  {self._trunk_diameter}cm")

    def produce_shade(self):
        print(
            f"Tree {self._name} now produces a shade of {self._height}cm long "
            f" and {self._trunk_diameter}cm wide."
        )


class Vegetable(Plant):
    def __init__(
        self,
        name: str,
        height: int,
        age: int,
        harvest_season: int,
        nutritional_value: int,
    ) -> None:
        super().__init__(name, height, age)
        self._harvest_season = harvest_season
        self._nutritional_value = nutritional_value

    def show(self):
        super().show()
        print(f"Harvest season: {self._harvest_season}")
        print(f"Nutritional value: {self._nutritional_value}")

    def grow(self, growth_rate):
        super().grow(growth_rate)

    def few_age(self):
        super().few_age()
        self._nutritional_value += 1


def main():
    print("=== Garden Plant Types ===")

    print("=== Flower")
    rose = Flower("Rose", 15.0, 10, "red")
    rose.show()
    print("[asking the rose to bloom]")
    rose.bloom()
    rose.show()
    print()

    print("=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    print()

    print("=== Vegetable")
    tomato = Vegetable("Tomato", 5.0, 10, "April", 0)
    tomato.show()
    print("[make tomato grow and age for 20 days]")
    for days in range(20):
        tomato.grow(2.1)
        tomato.few_age()
    tomato.show()


if __name__ == "__main__":
    main()
