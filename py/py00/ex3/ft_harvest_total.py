def ft_harvest_total() -> None:
    total = 0
    i = 1
    while (i <= 3):
        day = int(input("Day " + str(i) + " harvest: "))
        i += 1
        total += day
    print("Total harvest: ", total)
