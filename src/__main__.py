"""Entry point: uv run python -m src [options]."""
import argparse
import sys

from src.motor import Cam


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Function calling tool")
    parser.add_argument(
        "--functions_definition",
        default="data/input/functions_definition.json",
        help="functions definition JSON file",
    )
    parser.add_argument(
        "--input",
        default="data/input/function_calling_tests.json",
        help="prompts JSON file",
    )
    parser.add_argument(
        "--output",
        default="data/output/function_calling_results.json",
        help="results JSON file",
    )
    return parser.parse_args()


def main() -> int:
    """Run the program and return its exit code."""
    args = parse_args()
    try:
        return Cam(args.functions_definition, args.input, args.output).run()
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
