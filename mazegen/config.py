"""Load and validate maze configuration files."""
from dataclasses import dataclass


class ConfigError(Exception):
    """Represent an error while reading or validating a configuration."""


@dataclass
class MazeConfig:
    """Typed, validated representation of a maze configuration file."""

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None


_ALIASES: dict[str, str] = {
    "WIDTH": "WIDTH",
    "HEIGHT": "HEIGHT",
    "HAUTEUR": "HEIGHT",
    "ENTRY": "ENTRY",
    "ENTREE": "ENTRY",
    "EXIT": "EXIT",
    "SORTIE": "EXIT",
    "OUTPUT_FILE": "OUTPUT_FILE",
    "FICHIER_SORTIE": "OUTPUT_FILE",
    "PERFECT": "PERFECT",
    "SEED": "SEED",
    "GRAINE": "SEED",
}

_REQUIRED = ("WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE")


def _parse_coord(raw: str, key: str) -> tuple[int, int]:
    """Parse a coordinate from a ``x,y`` string.

    Raise ConfigError if the value is not a valid coordinate.
    """
    parts = raw.split(",")
    if len(parts) != 2:
        raise ConfigError(f"{key} must be formatted as 'x,y' (got: {raw!r})")
    try:
        x, y = int(parts[0].strip()), int(parts[1].strip())
    except ValueError as exc:
        raise ConfigError(
            f"{key} coordinates must be integers (got: {raw!r})"
        ) from exc
    return x, y


def _parse_bool(raw: str, key: str) -> bool:
    """Parse a boolean value from a string.

    Accept common true and false representations.
    """
    normalized = raw.strip().lower()
    if normalized in ("true", "1", "yes", "y"):
        return True
    if normalized in ("false", "0", "no", "n"):
        return False
    raise ConfigError(f"{key} must be a boolean (got: {raw!r})")


def _parse_int(raw: str, key: str) -> int:
    """Parse an integer from a string.

    Raise ConfigError if the value is not a valid integer.
    """
    try:
        return int(raw.strip())
    except ValueError as exc:
        raise ConfigError(f"{key} must be an integer (got: {raw!r})") from exc


def load_config(path: str) -> MazeConfig:
    """Load and validate a maze configuration file.

    Read the configuration file, validate its contents, and return a
    MazeConfig instance.

    Raise ConfigError if the file cannot be read or if the
    configuration is invalid.
    """
    try:
        with open(path, "r", encoding="utf-8") as handle:
            lines = handle.readlines()
    except OSError as exc:
        raise ConfigError(
            f"could not read config file '{path}': {exc}"
        ) from exc

    raw_values: dict[str, str] = {}
    for line_no, line in enumerate(lines, start=1):
        stripped = line.split("#")[0].strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            raise ConfigError(
                f"{path}:{line_no}: invalid syntax, expected KEY=VALUE "
                f"(got: {stripped!r})"
            )
        key, _, value = stripped.partition("=")
        key = key.strip().upper()
        value = value.strip()
        canonical = _ALIASES.get(key)
        if canonical is None:
            canonical = key
        raw_values[canonical] = value

    missing = [key for key in _REQUIRED if key not in raw_values]
    if missing:
        raise ConfigError(f"missing required key(s): {', '.join(missing)}")

    width = _parse_int(raw_values["WIDTH"], "WIDTH")
    height = _parse_int(raw_values["HEIGHT"], "HEIGHT")
    if width <= 0 or height <= 0:
        raise ConfigError("WIDTH and HEIGHT must be positive integers")

    entry = _parse_coord(raw_values["ENTRY"], "ENTRY")
    exit_ = _parse_coord(raw_values["EXIT"], "EXIT")
    for name, (x, y) in (("ENTRY", entry), ("EXIT", exit_)):
        if not (0 <= x < width and 0 <= y < height):
            raise ConfigError(f"{name} {(x, y)} is outside the maze bounds")
    if entry == exit_:
        raise ConfigError("ENTRY and EXIT must be different cells")

    output_file = raw_values["OUTPUT_FILE"]
    if not output_file:
        raise ConfigError("OUTPUT_FILE must not be empty")

    perfect_raw = raw_values.get("PERFECT")
    perfect: bool
    if perfect_raw is None or perfect_raw == "":
        perfect = True
    else:
        perfect = _parse_bool(perfect_raw, "PERFECT")

    seed_raw = raw_values.get("SEED")
    seed: int | None
    if seed_raw is None or seed_raw == "":
        seed = None
    else:
        seed = _parse_int(seed_raw, "SEED")

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit_,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
    )
