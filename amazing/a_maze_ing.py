import sys
from mazegen.config import Config
from mazegen.generator import MazeGenerator
from mazegen.solver import solve
from mazegen.writer import write_output
from mazegen.display import print_colored, WHITE, CYAN, YELLOW, GREEN, RED


COLORS = [WHITE, CYAN, YELLOW, GREEN, RED]
COLOR_NAMES = ["Blanc", "Cyan", "Jaune", "Vert", "Rouge"]


def menu(
    config: Config,
    maze: MazeGenerator,
    path: list,
    show_path: bool,
    wall_color: str,
) -> None:
    print("\n==== A-Maze-ing ====")
    print("1. Régénérer un nouveau labyrinthe")
    print("2. Afficher/masquer le chemin")
    print("3. Changer la couleur des murs")
    print("4. Quitter")
    print(f"Chemin visible : {'Oui' if show_path else 'Non'}")
    print(f"Couleur murs   : {COLOR_NAMES[COLORS.index(wall_color)]}")
    print("Choix (1-4) : ", end="")


def main() -> None:
    """Point d'entrée principal."""
    if len(sys.argv) != 2:
        print("Usage : python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        config = Config(sys.argv[1])

        show_path  = True
        wall_color = WHITE
        color_idx  = 0
        seed       = config.seed

        maze = MazeGenerator(
            width=config.width,
            height=config.height,
            seed=seed,
            perfect=config.perfect,
        )
        path = solve(maze, config.entry, config.exit)
        write_output(maze, config.output_file, config.entry, config.exit, path)
        print_colored(maze, config.entry, config.exit, path, show_path, wall_color)

        while True:
            menu(config, maze, path, show_path, wall_color)
            choice = input().strip()

            if choice == "1":
                # Régénérer avec une nouvelle graine
                seed = None
                maze = MazeGenerator(
                    width=config.width,
                    height=config.height,
                    seed=seed,
                    perfect=config.perfect,
                )
                path = solve(maze, config.entry, config.exit)
                write_output(
                    maze, config.output_file, config.entry, config.exit, path
                )
                print_colored(
                    maze, config.entry, config.exit, path, show_path, wall_color
                )

            elif choice == "2":
                show_path = not show_path
                print_colored(
                    maze, config.entry, config.exit, path, show_path, wall_color
                )

            elif choice == "3":
                color_idx = (color_idx + 1) % len(COLORS)
                wall_color = COLORS[color_idx]
                print_colored(
                    maze, config.entry, config.exit, path, show_path, wall_color
                )

            elif choice == "4":
                print("Au revoir !")
                sys.exit(0)

            else:
                print("Choix invalide, entre 1 et 4.")

    except (FileNotFoundError, ValueError) as e:
        print(f"Erreur : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()