"""Main program logic."""
import json
import os
import sys
import time

try:
    from pydantic import ValidationError
except ImportError:
    print(
        "Pydantic is not installed. "
        "Please install it using 'pip install pydantic'."
    )
    sys.exit(1)

from llm_sdk import Small_LLM_Model
from src.generator import CallGenerator, FunctionCall
from src.parser import Function, Prompt
from src.readfile import read_json
from src.vocab import Vocabulary

RED = "\033[91m"
RESET = "\033[0m"


def report(message: str) -> None:
    """Print an error message on stderr."""
    print(f"{RED}Error: {message}{RESET}", file=sys.stderr)


class Cam:
    """Reads the inputs, generates every function call, writes the output."""

    def __init__(
        self, functions_path: str, input_path: str, output_path: str
    ) -> None:
        """Store the three file paths.

        Args:
            functions_path: functions definition JSON file.
            input_path: prompts JSON file.
            output_path: results JSON file to write.
        """
        self.functions_path = functions_path
        self.input_path = input_path
        self.output_path = output_path

    def _load_functions(self) -> list[Function]:
        """Load and validate the function definitions."""
        data = read_json(self.functions_path)
        if not isinstance(data, list) or not data:
            raise ValueError(
                f"{self.functions_path} must contain a non-empty JSON list"
            )
        functions: list[Function] = []
        for item in data:
            try:
                functions.append(Function.model_validate(item))
            except ValidationError as error:
                raise ValueError(
                    f"Invalid function definition: {item!r}"
                ) from error
        return functions

    def _load_prompts(self) -> list[Prompt]:
        """Load the prompts, skipping invalid entries with a warning."""
        data = read_json(self.input_path)
        if not isinstance(data, list):
            raise ValueError(f"{self.input_path} must contain a JSON list")
        prompts: list[Prompt] = []
        for item in data:
            try:
                prompts.append(Prompt.model_validate(item))
            except ValidationError:
                report(f"skipping invalid prompt entry: {item!r}")
        return prompts

    def _write(self, calls: list[FunctionCall]) -> None:
        """Write the results file, creating its folder if needed."""
        folder = os.path.dirname(self.output_path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(self.output_path, "w", encoding="utf-8") as file:
            json.dump(
                [call.model_dump() for call in calls],
                file,
                indent=4,
                ensure_ascii=False,
            )

    def run(self) -> int:
        """Run the whole pipeline.

        Returns:
            0 on success, 1 if the program could not run.
        """
        try:
            functions = self._load_functions()
            prompts = self._load_prompts()
        except ValueError as error:
            report(str(error))
            return 1

        if not prompts:
            report("no valid prompt to process")
            return 1

        try:
            model = Small_LLM_Model()
            vocab = Vocabulary.load(model.get_path_to_vocab_file())
        except Exception as error:
            report(f"cannot load the model: {error}")
            return 1

        generator = CallGenerator(model, vocab, functions)
        calls: list[FunctionCall] = []
        start = time.time()
        for number, prompt in enumerate(prompts, 1):
            print(f"[{number}/{len(prompts)}] {prompt.prompt}")
            try:
                calls.append(generator.generate(prompt))
            except Exception as error:
                report(f"prompt skipped ({error})")

        try:
            self._write(calls)
        except OSError as error:
            report(f"cannot write {self.output_path}: {error}")
            return 1
        print(
            f"{len(calls)}/{len(prompts)} calls written to "
            f"{self.output_path} in {time.time() - start:.1f}s"
        )
        return 0
