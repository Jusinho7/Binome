from pathlib import Path
from typing import Optional
from subprocess import run
from time import sleep
try:
    from rich.console import Console
except ImportError as exc:
    raise SystemExit(
        "Error: The 'rich' library is not installed. "
        "Please install it using 'pip install rich' and try again."
    ) from exc

BASE_DIR = Path(__file__).resolve().parent
DOSSIER_MAPS = BASE_DIR / "../maps"

console = Console()


class MapSelector:
    """Display the available maps and return the file selected by the user."""

    def __init__(self, maps_directory: Path = DOSSIER_MAPS) -> None:
        self.maps_directory = maps_directory

    def select(self) -> Optional[Path]:
        folders = self._get_map_folders()
        if not folders:
            return None

        while True:
            selected_folder, go_back = self._select_item(
                folders, "Choice map", "folder"
            )
            if go_back:
                console.print("[bold cyan]Goodbye![/bold cyan]")
                sleep(1)
                run(["clear"])
                return None
            if selected_folder is None:
                return None

            files = sorted(selected_folder.glob("*.txt"))
            if not files:
                console.print(
                    f"[bold red]No .txt files found in[/bold red] "
                    f"[yellow]{selected_folder}[/yellow]"
                )
                continue

            selected_file, go_back = self._select_item(
                files,
                "Choice file",
                "file"
            )
            if go_back:
                console.print("[dim]Returning to map selection.[/dim]")
                continue
            if selected_file is None:
                return None

            console.print(
                f"[bold green]Selected file:[/bold green] "
                f"[cyan]{selected_file}[/cyan]"
            )
            return selected_file

    def _get_map_folders(self) -> list[Path]:
        if (
            not self.maps_directory.exists()
            or not self.maps_directory.is_dir()
        ):
            console.print(
                f"[bold red]Maps directory not found:[/bold red] "
                f"[yellow]{self.maps_directory}[/yellow]"
            )
            return []

        folders = sorted(
            path
            for path in self.maps_directory.iterdir()
            if path.is_dir()
        )
        if not folders:
            console.print(
                f"[bold red]No map folders found in[/bold red] "
                f"[yellow]{self.maps_directory}[/yellow]"
            )
        return folders

    @staticmethod
    def _select_item(
        items: list[Path], title: str, item_type: str
    ) -> tuple[Optional[Path], bool]:
        console.print(f"\n[bold cyan]--- {title} ---[/bold cyan]")
        for index, item in enumerate(items, 1):
            console.print(
                f"  [bold yellow]{index}.[/bold yellow]"
                f" [white]{item.name}[/white]"
            )
        console.print("  [bold red]0.[/bold red] [dim]Annuler[/dim]")
        console.print("  [bold magenta]R.[/bold magenta] [dim]Retour[/dim]")

        while True:
            choice = console.input(
                "[bold green]Your choice[/bold green] : "
            ).strip()
            if choice == "0":
                console.print("[dim]Selection cancelled.[/dim]")
                return None, False

            if choice.lower() == "r":
                return None, True

            if choice.isdigit() and 1 <= int(choice) <= len(items):
                return items[int(choice) - 1], False

            console.print(f"[bold red]Invalid {item_type} choice.[/bold red]")


def choice_map() -> Optional[Path]:
    """Keep the original function API for callers outside this module."""
    return MapSelector().select()
