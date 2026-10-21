import json
from pathlib import Path
import os

LINK = "data/input/function_calling_tests.json"
FILE = Path(__file__).resolve().parent.parent / LINK

LINK_2 = "data/input/function_definition.json"
FILE_2 = Path(__file__).resolve().parent.parent / LINK_2

RED = "\033[91m"
RESET = "\033[0m"


class ReadFile:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def read(self) -> dict[str, any] | None:
        try:
            if not os.path.exists(self.file_path):
                print(f"{RED}File does not exist: {self.file_path} {RESET}")
                return None
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"{RED}File not found: {self.file_path} {RESET}")
            return None
        except json.JSONDecodeError:
            print(
                f"{RED}Error decoding JSON from file: {self.file_path} {RESET}"
            )
            return None
