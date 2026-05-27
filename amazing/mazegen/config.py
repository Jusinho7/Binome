# mazegen/config.py
from typing import Tuple
import os


class Config:
    def __init__(self, filepath: str) -> None:
        self._data = self._parse(filepath)
        self.width       = self._get_int("WIDTH")
        self.height      = self._get_int("HEIGHT")
        self.entry       = self._get_coords("ENTRY")
        self.exit        = self._get_coords("EXIT")
        self.output_file = self._get_str("OUTPUT_FILE")
        self.perfect     = self._get_bool("PERFECT")
        self.seed        = self._get_int("SEED", required=False)
        self._validate()

    def _parse(self, filepath: str) -> dict:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Fichier introuvable : {filepath}")

        data = {}
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ValueError(f"Ligne invalide : {line}")
                key, value = line.split("=", 1)
                data[key.strip()] = value.strip()
        return data

    def _get_int(self, key: str, required: bool = True) -> int:
        if key not in self._data:
            if not required:
                return None
            raise ValueError(f"Clé manquante : {key}")
        try:
            return int(self._data[key])
        except ValueError:
            raise ValueError(f"{key} doit être un entier")

    def _get_str(self, key: str) -> str:
        if key not in self._data:
            raise ValueError(f"Clé manquante : {key}")
        return self._data[key]

    def _get_bool(self, key: str) -> bool:
        if key not in self._data:
            raise ValueError(f"Clé manquante : {key}")
        return self._data[key].lower() == "true"

    def _get_coords(self, key: str) -> Tuple[int, int]:
        if key not in self._data:
            raise ValueError(f"Clé manquante : {key}")
        try:
            x, y = self._data[key].split(",")
            return int(x.strip()), int(y.strip())
        except ValueError:
            raise ValueError(f"{key} doit être au format x,y")

    def _validate(self) -> None:
        if self.width < 2 or self.height < 2:
            raise ValueError("Le labyrinthe doit faire au moins 2x2")
        ex, ey = self.entry
        if not (0 <= ex < self.width and 0 <= ey < self.height):
            raise ValueError("ENTRY est hors des limites")
        ox, oy = self.exit
        if not (0 <= ox < self.width and 0 <= oy < self.height):
            raise ValueError("EXIT est hors des limites")
        if self.entry == self.exit:
            raise ValueError("ENTRY et EXIT doivent être différents")