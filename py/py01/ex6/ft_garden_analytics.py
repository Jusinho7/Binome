class Plant:
    class __Stats:
        def __init__(self):
            self.grow_calls = 0
            self.age_calls = 0
            self.show_calls = 0

        def display(self):
            print(f"Stats: {self.grow_calls} grow,"
                  f" {self.age_calls} age,"
                  f" {self.show_calls} show")

    def __init__(self, name: str, height: float, age: int):
        self.name = name
        self.height = height
        self.age = age
        self._stats = Plant.__Stats()

    @staticmethod
    def is_older_than_a_year(age: int) -> bool:
        return age > 365

    @classmethod
    def anonymous(cls):
        return cls("Unknown plant", 0.0, 0)

    def grow(self):
        self._stats.grow_calls += 1
        self.height += 30.0

    def age_plant(self):
        self._stats.age_calls += 1
        self.age += 20

    def show(self):
        self._stats.show_calls += 1
        print(f"{self.name}: {self.height}cm, {self.age} days old")

    def display_stats(self):
        print(f"[statistics for {self.name}]")
        self._stats.display()


class Flower(Plant):
    def __init__(self, name: str, height: float, age: int, color: str):
        super().__init__(name, height, age)
        self.color = color
        self.bloomed = False

    def bloom(self):
        self.bloomed = True

    def show(self):
        super().show()
        print(f"Color: {self.color}")
        if self.bloomed:
            print(f"{self.name} is blooming beautifully!")
        else:
            print(f"{self.name} has not bloomed yet")


class Tree(Plant):
    class __TreeStats:
        def __init__(self):
            self.shade_calls = 0

        def display(self):
            print(f"{self.shade_calls} shade")

    def __init__(
        self,
        name: str,
        height: float,
        age: int,
        trunk_diameter: float
    ):
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter
        self.__tree_stats = Tree.__TreeStats()

    def produce_shade(self):
        self.__tree_stats.shade_calls += 1
        print(f"Tree {self.name} now produces a shade of"
              f" {self.height}cm long and {self.trunk_diameter}cm wide.")

    def show(self):
        super().show()
        print(f"Trunk diameter: {self.trunk_diameter}cm")

    def display_stats(self):
        super().display_stats()
        self.__tree_stats.display()


class Seed(Flower):
    def __init__(
        self,
        name: str,
        height: float,
        age: int,
        color: str,
        seeds: int = 0
    ):
        super().__init__(name, height, age, color)
        self.seeds = seeds

    def show(self):
        super().show()
        print(f"Seeds: {self.seeds}")


def display_stats(plant: Plant):
    plant.display_stats()


def main():
    print("=== Garden statistics ===")

    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> {Plant.is_older_than_a_year(30)}")
    print(
        f"Is 400 days more than a year? -> {Plant.is_older_than_a_year(400)}"
    )

    print("=== Flower")
    rose = Flower("Rose", 15.0, 10, "red")
    rose.show()
    display_stats(rose)

    print("[asking the rose to grow and bloom]")
    rose.grow()
    rose.bloom()
    rose.show()
    display_stats(rose)

    print("=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    display_stats(oak)

    print("[asking the oak to produce shade]")
    oak.produce_shade()
    display_stats(oak)

    print("=== Seed")
    sunflower = Seed("Sunflower", 80.0, 45, "yellow", 0)
    sunflower.show()

    print("[make sunflower grow, age and bloom]")
    sunflower.grow()
    sunflower.age_plant()
    sunflower.bloom()
    sunflower.seeds = 42
    sunflower.show()
    display_stats(sunflower)

    print("=== Anonymous")
    anon = Plant.anonymous()
    anon.show()
    display_stats(anon)


if __name__ == "__main__":
    main()
