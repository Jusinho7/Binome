import importlib.util
from pathlib import Path

ex1_dir = Path(__file__).resolve().parents[1] / "mnt" / "user-data" / "outputs" / "datadeck" / "ex1"
module_path = ex1_dir / "creatures.py"

spec = importlib.util.spec_from_file_location("datadeck_ex1_creatures", module_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Unable to load ex1 creatures from {module_path}")

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

Sproutling = module.Sproutling
Bloomelle = module.Bloomelle
Shiftling = module.Shiftling
Morphagon = module.Morphagon

__all__ = ["Sproutling", "Bloomelle", "Shiftling", "Morphagon"]
