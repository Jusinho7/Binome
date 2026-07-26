"""Unit tests for the config module (run with pytest)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest  # noqa: E402

from config import ConfigError, load_config  # noqa: E402


def _write(tmp_path: Path, content: str) -> str:
    path = tmp_path / "config.txt"
    path.write_text(content, encoding="utf-8")
    return str(path)


def test_valid_config(tmp_path: Path) -> None:
    path = _write(
        tmp_path,
        "WIDTH=20\nHEIGHT=15\nENTRY=0,0\nEXIT=19,14\n"
        "OUTPUT_FILE=maze.txt\nPERFECT=True\nSEED=42\n# comment\n",
    )
    cfg = load_config(path)
    assert cfg.width == 20
    assert cfg.height == 15
    assert cfg.entry == (0, 0)
    assert cfg.exit == (19, 14)
    assert cfg.output_file == "maze.txt"
    assert cfg.perfect is True
    assert cfg.seed == 42


def test_missing_key_raises(tmp_path: Path) -> None:
    path = _write(tmp_path, "WIDTH=20\nHEIGHT=15\n")
    with pytest.raises(ConfigError):
        load_config(path)


def test_missing_file_raises() -> None:
    with pytest.raises(ConfigError):
        load_config("/does/not/exist.txt")


def test_malformed_line_raises(tmp_path: Path) -> None:
    path = _write(tmp_path, "WIDTH 20\n")
    with pytest.raises(ConfigError):
        load_config(path)


def test_same_entry_exit_raises(tmp_path: Path) -> None:
    path = _write(
        tmp_path,
        "WIDTH=5\nHEIGHT=5\nENTRY=0,0\nEXIT=0,0\n"
        "OUTPUT_FILE=out.txt\nPERFECT=True\n",
    )
    with pytest.raises(ConfigError):
        load_config(path)


def test_out_of_bounds_raises(tmp_path: Path) -> None:
    path = _write(
        tmp_path,
        "WIDTH=5\nHEIGHT=5\nENTRY=0,0\nEXIT=9,9\n"
        "OUTPUT_FILE=out.txt\nPERFECT=True\n",
    )
    with pytest.raises(ConfigError):
        load_config(path)
