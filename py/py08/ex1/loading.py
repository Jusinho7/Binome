#!/usr/bin/env python3
import importlib
import sys
from importlib.metadata import version, PackageNotFoundError
from typing import Any, Optional


def show_dependencies(name: str, description: str) -> Optional[Any]:
    try:
        module = importlib.import_module(name)
    except (ModuleNotFoundError, ImportError):
        print(f"[MISSING] {name} - {description}")
        return None
    print(f"[OK] {name} - {description} ready")
    return module


def show_versions(package_names: list) -> None:
    print("\nInstalled package versions:")
    for name in package_names:
        try:
            ver = version(name)
            print(f"  {name}: {ver}")
        except PackageNotFoundError:
            print(f"  {name}: not installed")


def show_setup_guide() -> None:
    print("\nMissing dependencies detected.\n")
    print("pip:")
    print("    pip install -r requirements.txt\n")
    print("Poetry:")
    print("    poetry install")
    print("    poetry run python loading.py\n")


def show_dependency_comparison() -> None:
    print("\nDependency Managers")
    print("-------------------")
    print("pip")
    print("  • Reads dependencies from requirements.txt")
    print("  • Can install packages globally or in a virtual environment")
    print("  • Dependency versions are managed manually")
    print("  • Does not generate a lock file by default\n")
    print("Poetry")
    print("  • Uses pyproject.toml as the project configuration")
    print("  • Resolves dependency versions automatically")
    print("  • Creates and manages isolated virtual environments")
    print("  • Stores exact versions in poetry.lock")


def fetch_matrix_data_from_api(requests_module: Any) -> Optional[dict]:
    try:
        response = requests_module.get(
            "https://api.github.com/repos/python/cpython", timeout=5
        )
        response.raise_for_status()
        payload = response.json()
        return {"seed": payload.get("stargazers_count", 42)}
    except Exception as exc:
        print(f"API fetch failed ({exc}); falling back to numpy simulation.")
        return None


def analyze_data(
        pd: Any, np: Any, plt: Any, seed: Optional[int] = None) -> None:
    print("\nAnalyzing Matrix data...")
    if seed is not None:
        np.random.seed(seed % (2**32 - 1))
    data = np.random.normal(loc=50, scale=10, size=1000)
    df = pd.DataFrame({"signal": data})
    print(f"Processing {len(df)} data points...")
    df["average"] = df["signal"].rolling(20).mean()
    plt.figure(figsize=(10, 5))
    plt.bar(df.index, df["signal"], width=1.0, alpha=0.6, color="black")
    plt.plot(df["average"], linewidth=2, color="red", label="Rolling Average")
    plt.title("Matrix Signal")
    plt.xlabel("Sample")
    plt.ylabel("Value")
    plt.legend()
    plt.tight_layout()
    plt.savefig("matrix_analysis.png")
    plt.close()
    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")


def main() -> None:
    use_api = "--api" in sys.argv
    print("LOADING STATUS: Loading programs...\n")
    print("Checking dependencies:")
    pd = show_dependencies("pandas", "Data manipulation")
    np = show_dependencies("numpy", "Numerical computation")
    plt = show_dependencies("matplotlib.pyplot", "Visualization")
    if use_api:
        requests_module = show_dependencies("requests", "Network access")
    if pd is None or np is None or plt is None:
        show_setup_guide()
        show_dependency_comparison()
        sys.exit(1)
    packages = ["pandas", "numpy", "matplotlib"]
    if use_api:
        packages.append("requests")
    show_versions(packages)
    show_dependency_comparison()
    seed = None
    if use_api and requests_module is not None:
        result = fetch_matrix_data_from_api(requests_module)
        if result is not None:
            seed = result["seed"]
    analyze_data(pd, np, plt, seed=seed)


if __name__ == "__main__":
    main()
