#!/usr/bin/env python3

"""
Helper file for Growing Code.

This file helps you test your exercises easily.
Just run: python3 main.py
"""

import sys
import os

# Ajout automatique de tous les dossiers ex00 à ex09
for i in range(10):
    folder = f"ex{i}"
    if os.path.isdir(folder):
        sys.path.append(folder)


def test_ft_exercise(exercise_file_name):
    """
    This function tries to run one of your exercises.
    """
    print(f"\n=== Testing {exercise_file_name} ===")

    try:
        # Recharger le module si déjà importé
        if exercise_file_name in sys.modules:
            del sys.modules[exercise_file_name]

        ft_module = __import__(exercise_file_name)
        ft_function = getattr(ft_module, exercise_file_name)

        if exercise_file_name == "ft_seed_inventory":
            print("Testing with different seed types and units:\n")
            ft_function("tomato", 15, "packets")
            ft_function("carrot", 8, "grams")
            ft_function("lettuce", 12, "area")
            print("\nTesting with unknown unit:")
            ft_function("basil", 5, "unknown")
        else:
            ft_function()

    except ImportError:
        print(f"❌ Could not find {exercise_file_name}.py")
        print("   Make sure your file exists in the right ex0X/ folder")

    except AttributeError:
        print(f"❌ Could not find function {exercise_file_name}() in your file")
        print(f"   Make sure you have: def {exercise_file_name}():")

    except TypeError as error:
        msg = str(error)
        print(f"❌ Type error: {error}")
        if exercise_file_name == "ft_seed_inventory":
            if "missing" in msg and "required positional argument" in msg:
                print("   For exercise 7, make sure your function takes parameters:")
                print(
                    f"   def {exercise_file_name}"
                    "(seed_type: str, quantity: int, unit: str) -> None:"
                )
        else:
            print("   Your function should not take any parameters")

    except Exception as error:
        print(f"❌ Error running your function: {error}")
        print("   Check your code for syntax errors")


def main():
    """Run main function."""
    print("🌱 Welcome to Growing Code! 🌱")
    print("This helper will test your exercises for you.")
    print("\nWhich exercise would you like to test?")
    print()
    print("0 - ft_hello_garden     (Say hello to the garden community)")
    print("1 - ft_garden_name      (Display garden name)")
    print("2 - ft_plot_area        (Calculate garden plot area)")
    print("3 - ft_harvest_total    (Add up harvest weights)")
    print("4 - ft_plant_age        (Check if plant is ready)")
    print("5 - ft_water_reminder   (Check if plants need water)")
    print("6 - ft_count_harvest    (Count days to harvest)")
    print("7 - ft_seed_inventory   (Seed inventory with type hints)")
    print("a - test all exercises")
    print()

    choice = input("Enter your choice: ")

    if choice == "0":
        test_ft_exercise("ft_hello_garden")
    elif choice == "1":
        test_ft_exercise("ft_garden_name")
    elif choice == "2":
        test_ft_exercise("ft_plot_area")
    elif choice == "3":
        test_ft_exercise("ft_harvest_total")
    elif choice == "4":
        test_ft_exercise("ft_plant_age")
    elif choice == "5":
        test_ft_exercise("ft_water_reminder")
    elif choice == "6":
        test_ft_exercise("ft_count_harvest_iterative")
        test_ft_exercise("ft_count_harvest_recursive")
    elif choice == "7":
        test_ft_exercise("ft_seed_inventory")
    elif choice == "a":
        test_ft_exercise("ft_hello_garden")
        test_ft_exercise("ft_garden_name")
        test_ft_exercise("ft_plot_area")
        test_ft_exercise("ft_harvest_total")
        test_ft_exercise("ft_plant_age")
        test_ft_exercise("ft_water_reminder")
        test_ft_exercise("ft_count_harvest_iterative")
        test_ft_exercise("ft_count_harvest_recursive")
        test_ft_exercise("ft_seed_inventory")
    else:
        print("❌ Invalid choice! Please enter 0, 1, 2, 3, 4, 5, 6, 7, or a")


if __name__ == "__main__":
    main()