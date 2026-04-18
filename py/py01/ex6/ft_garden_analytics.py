class Plant:
    class __stats:
        def __init__(self) -> None:
            self.grow_calls = 0
            self.age_calls = 0
            self.show_calls = 0

        def display(self) -> None:
            print(
                f"Stats:"
                f" {self.grow_calls} grow,"
                f" {self.age_calls} age,"
                f" {self.show_calls} show"
            )

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
        self.__stats = Plant.__stats()

    def grow(self) -> None:
        self.__stats.grow_calls += 1
        self.age += 1

    def age_plant(self) -> None:
        self.__stats.age_calls += 1

    @staticmethod
    def is_mature(age: int) -> bool:
        return age > 12

    @classmethod
    def anonymous(cls) -> "Plant":
        return cls(name="Unknown", age=0)

    def show(self) -> None:
        print(
            f"Plant  → name: {self.name} |"
            f" age: {self.age} months |"
            f" mature: {self.is_mature(self.age)}"
        )


class Seed(Plant):
    def __init__(self, name: str, age: int, seed_counter: int = 0) -> None:
        super().__init__(name, age)
        self.seed_counter = seed_counter

    def show(self) -> None:
        super().show()
        print(f"Seeds: {self.seed_counter}")


def main():
    print("=== Test Plant ===")
    plant1 = Plant("Rose", 15)
    plant2 = Plant("Oak", 10)
    plant3 = Plant.anonymous()

    plant1.show()
    plant2.show()
    plant3.show()

    print()
    print("=== Test Seed ===")
    seed1 = Seed("Sunflower", 14, 250)
    seed2 = Seed("Tulip", 8, 50)
    seed3 = Seed.anonymous()

    seed1.show()
    print()
    seed2.show()
    print()
    seed3.show()


if __name__ == "__main__":
    main()
