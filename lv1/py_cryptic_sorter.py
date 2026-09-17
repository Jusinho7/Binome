def cryptic_sorter(strings: list[str]) -> list[str]:
    return sorted(
        strings,
        key=lambda x: (len(x), not x.islower(), sum(i in "aeuioy" for i in x.lower()))
    )


if __name__ == "__main__":
    print(cryptic_sorter(["apple","cat","banana", "dOg", "dog", "DOG","elephant"]))