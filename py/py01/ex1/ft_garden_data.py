class Plant:
    def __init__(self):
        self.name = None
        self.height = None
        self.age = None

    def show(self):
        print(f"{self.name}: {self.height} cm {self.age} days old")


def main():
    print("=== Garden Plant Registry ===")

    rose = Plant()
    rose.name = "Rose"
    rose.height = 25
    rose.age = 30
    rose.show()

    sunflower = Plant()
    sunflower.name = "Sunflower"
    sunflower.height = 80
    sunflower.age = 45
    sunflower.show()

    cactus = Plant()
    cactus.name = "Cactus"
    cactus.height = 15
    cactus.age = 120
    cactus.show()


if __name__ == "__main__":
    main()
