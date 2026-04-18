def helper(day: int, i: int = 1) -> None:
    if i > day:
        print("Harvest time!")
        return
    print("Day ", i)
    helper(day, i + 1)


def ft_count_harvest_recursive() -> None:
    day = int(input("Days until harvest: "))
    helper(day)
