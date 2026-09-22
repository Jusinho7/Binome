from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent
DOSSIER_MAPS = BASE_DIR / "../maps"
RED = "\033[31m"
RESET = "\033[0m"
ORANGE = "\033[33m"
MARRON = "\033[33m"


class MapSelector:
    """Display the available maps and return the file selected by the user."""

    def __init__(self, maps_directory: Path = DOSSIER_MAPS) -> None:
        self.maps_directory = maps_directory

    def select(self) -> Optional[Path]:
        folders = self._get_map_folders()
        if not folders:
            return None

        selected_folder = self._select_item(folders, "Choice map", "folder")
        if selected_folder is None:
            return None

        files = sorted(selected_folder.glob("*.txt"))
        if not files:
            print(f"{RED}No .txt files found in{RESET}", selected_folder)
            return None

        selected_file = self._select_item(files, "Choice file", "file")
        if selected_file is not None:
            print("Selected file:", selected_file)
        return selected_file

    def _get_map_folders(self) -> list[Path]:
        if not self.maps_directory.exists() or not self.maps_directory.is_dir():
            print(f"{RED}Maps directory not found{RESET}", self.maps_directory)
            return []

        folders = sorted(path for path in self.maps_directory.iterdir() if path.is_dir())
        if not folders:
            print(f"{RED}No map folders found{RESET}", self.maps_directory)
        return folders

    @staticmethod
    def _select_item(items: list[Path], title: str, item_type: str) -> Optional[Path]:
        print(f"\n--- {title} ---")
        for index, item in enumerate(items, 1):
            print(f"  {index}. {item.name}")
        print("  0. Annuler")

        while True:
            choice = input("Your choice : ").strip()
            if choice == "0":
                return None

            if choice.isdigit() and 1 <= int(choice) <= len(items):
                return items[int(choice) - 1]

            print(f"Invalid {item_type} choice.")


def choice_map() -> Optional[Path]:
    """Keep the original function API for callers outside this module."""
    return MapSelector().select()
