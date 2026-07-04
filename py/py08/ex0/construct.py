#!/usr/bin/env python3
import sys
import os
import site


def is_venv() -> bool:
    return sys.prefix != sys.base_prefix


def show_inside() -> None:
    venv_path = sys.prefix
    venv_name = os.path.basename(venv_path)
    site_packages = site.getsitepackages()
    print("MATRIX STATUS: Welcome to the construct\n")
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {venv_name}")
    print(f"Environment Path: {venv_path}\n")
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting the global system.")
    print(f"\nPackage installation path:\n {site_packages[0]}")


def show_outside() -> None:
    print("MATRIX STATUS: You're still plugged in\n")
    print("Current Python:", sys.executable)
    print("Virtual Environment: None detected\n")
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.\n")
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print("matrix_env\\Scripts\\activate  # On Windows\n")
    print("Then run this program again.")


def main() -> None:
    show_inside() if is_venv() else show_outside()


if __name__ == "__main__":
    main()
