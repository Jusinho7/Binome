def ft_water_reminder() -> None:
    day = int(input("Day since last watering: "))
    if day > 2:
        print("Water the plans!")
    else:
        print("Plants are fine")
