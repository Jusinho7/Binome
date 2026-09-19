import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MAPS_DIR = ROOT / "maps"


def list_maps() -> list[Path]:
    files: list[Path] = []
    for path in sorted(MAPS_DIR.rglob("*.txt")):
        if path.is_file():
            files.append(path)
    return files

def print_menu(maps: list[Path]) -> None:
    print("\nChoisir une carte pour lancer Fly-in")
    print("=" * 42)
    for index, map_path in enumerate(maps, start=1):
        rel = map_path.relative_to(ROOT)
        print(f"  {index}. {rel}")
    print("  0. Quitter")
    print("=" * 42)

def prompt_choice(maps: list[Path]) -> int:
    while True:
        try:
            choice = input("\nVotre choix: ").strip()
            if choice == "":
                continue
            value = int(choice)
            if 0 <= value <= len(maps):
                return value
            print("Choix invalide. Réessayez.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

def main() -> int:
    maps = list_maps()
    if not maps:
        print("Aucune carte trouvée dans le dossier maps/.")
        return 1

    print_menu(maps)
    choice = prompt_choice(maps)
    if choice == 0:
        print("Annulé.")
        return 0

    selected = maps[choice - 1]
    rel_path = selected.relative_to(ROOT)
    print(f"\nCarte sélectionnée: {rel_path}")

    env = os.environ.copy()
    env["MAP"] = str(rel_path)
    subprocess.run(["make", "run"], cwd=str(ROOT), env=env, check=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
