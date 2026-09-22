from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent
DOSSIER_MAPS = BASE_DIR / "../maps"
RED = "\033[31m"
RESET = "\033[0m"
ORANGE = "\033[33m"
MARRON = "\033[33m"


def choice_map() -> Optional[Path]:
    if not DOSSIER_MAPS.exists() or not DOSSIER_MAPS.is_dir():
        print(f"{RED}Maps directory not found{RESET}", DOSSIER_MAPS)
        return None
    folders = sorted(DOSSIER_MAPS.glob("*"))

    if not folders:
        print(f"{RED}No map folders found{RESET}", DOSSIER_MAPS)
        return None

    print("\n--- Choice map ---")
    for i, folder in enumerate(folders, 1):
        print(f"  {i}. {folder.name}")
    print("  0. Annuler")

    while True:
        choice = input("Your choice : ").strip()

        if choice == "0":
            return None

        if choice == "1":
            print(
                f"{MARRON}README is available in the maps folder.{RESET}"
                f"{MARRON}Please read it for instructions.{RESET}"
            )
            print(f"{MARRON}Please read it for instructions.{RESET}")
            return None

        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(folders):
                selected_folder = folders[index - 1]
                break
        return None

        print("Invalid choice.")

    files = sorted(selected_folder.glob("*.txt"))

    if not files:
        print(f"{RED}No .txt files found in{RESET}", selected_folder)
        return None

    print("\n--- Choice file ---")
    for i, file in enumerate(files, 1):
        print(f"  {i}. {file.name}")
    print("  0. Annuler")

    while True:
        choice = input("Your choice : ").strip()

        if choice == "0":
            return None

        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(files):
                print("Selected file:", files[index - 1])
                file_choice = files[index - 1]
                break

        print("Invalid choice.")

    return file_choice
