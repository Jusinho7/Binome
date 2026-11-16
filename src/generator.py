"""Function call generation with constrained decoding."""
import json
from typing import Any

from pydantic import BaseModel

from llm_sdk import Small_LLM_Model
from src.constraints import (
    NUMBER_CHARS,
    generate_choice,
    is_number_complete,
    is_number_prefix,
    pick_token,
)
from src.parser import Function, Prompt
from src.prompt import build_prompt
from src.vocab import Vocabulary

MAX_NUMBER_CHARS = 20
MAX_STRING_TOKENS = 48


def find_loop(tokens: list[int]) -> int:
    """Detect a block of tokens repeated three times in a row.

    Args:
        tokens: token ids generated so far for the current string.

    Returns:
        The size of the repeating block, or 0 if there is no loop.
    """
    for size in range(2, 9):
        if len(tokens) >= 3 * size and (
            tokens[-size:] == tokens[-2 * size:-size]
            == tokens[-3 * size:-2 * size]
        ):
            return size
    return 0


class FunctionCall(BaseModel):
    """One generated function call (one entry of the output file)."""

    prompt: str
    name: str
    parameters: dict[str, Any]


class CallGenerator:
    """Turns prompts into function calls using constrained decoding."""

    def __init__(
        self,
        model: Small_LLM_Model,
        vocab: Vocabulary,
        functions: list[Function],
    ) -> None:
        """Precompute the token sets used by the masks.

        Args:
            model: the LLM wrapper.
            vocab: decoded vocabulary.
            functions: the available functions.
        """
        self.model = model
        self.vocab = vocab
        self.function_list = functions
        self.functions = {f.name: f for f in functions}
        self.targets = [f.name + '"' for f in functions]
        texts = vocab.texts
        self.number_tokens = {
            i: t for i, t in enumerate(texts)
            if t
            and t.lstrip(" ")
            and len(t) - len(t.lstrip(" ")) <= 1
            and set(t.lstrip(" ")) <= NUMBER_CHARS
        }
        self.number_stop = {
            i for i, t in enumerate(texts) if t and t[0] in ",}"
        }
        self.string_tokens = [
            i for i, t in enumerate(texts)
            if t and '"' not in t and all(ord(c) >= 32 for c in t)
        ]
        self.quote_tokens = {
            i for i, t in enumerate(texts) if t and t[0] == '"'
        }
        self.quote_id = vocab.index['"'][0]

    def _append(self, ids: list[int], text: str) -> None:
        """Force `text` into the context (no choice for the model)."""
        if text:
            ids.extend(self.model.encode(text)[0].tolist())

    def _number(self, ids: list[int], integer: bool) -> int | float:
        """Let the model write a number, one valid token at a time."""
        value = ""
        while len(value) < MAX_NUMBER_CHARS:
            allowed = [
                i for i, t in self.number_tokens.items()
                if (not value or t[0] != " ")
                and is_number_prefix(value + t.lstrip(" "), integer)
            ]
            if is_number_complete(value, integer):
                allowed += list(self.number_stop)
            if not allowed:
                break
            logits = self.model.get_logits_from_input_ids(ids)
            token = pick_token(logits, allowed)
            if token in self.number_stop:
                break
            ids.append(token)
            value += self.number_tokens[token].lstrip(" ")
        if not is_number_complete(value, integer):
            raise ValueError(f"Could not generate a number: {value!r}")
        return int(value) if integer else float(value)

    def _string(self, ids: list[int]) -> str:
        """Let the model write a string until it closes the quote."""
        allowed = self.string_tokens + list(self.quote_tokens)
        made: list[int] = []
        for _ in range(MAX_STRING_TOKENS):
            logits = self.model.get_logits_from_input_ids(ids)
            token = pick_token(logits, allowed)
            if token in self.quote_tokens:
                break
            ids.append(token)
            made.append(token)
            size = find_loop(made)
            if size:
                del made[-2 * size:]
                del ids[-2 * size:]
                break
        ids.append(self.quote_id)
        value = "".join(self.vocab.texts[t] or "" for t in made)
        try:
            return str(json.loads(f'"{value}"'))
        except json.JSONDecodeError:
            return value

    def _value(self, ids: list[int], type_name: str) -> Any:
        """Generate one value of the given schema type."""
        if type_name == "number":
            return self._number(ids, integer=False)
        if type_name == "integer":
            return self._number(ids, integer=True)
        if type_name == "string":
            return self._string(ids)
        if type_name == "boolean":
            choice = generate_choice(
                self.model, self.vocab, ids, ["true", "false"]
            )
            return choice == "true"
        raise ValueError(f"Unsupported parameter type: {type_name}")

    def generate(self, prompt: Prompt) -> FunctionCall:
        """Generate the function call matching a prompt.

        Args:
            prompt: the user request.

        Returns:
            The chosen function name and its typed parameters.

        Raises:
            ValueError: if a value cannot be generated.
        """
        text = build_prompt(prompt, self.function_list)
        ids = self.model.encode(text)[0].tolist()
        self._append(ids, '{"name": "')
        name = generate_choice(
            self.model, self.vocab, ids, self.targets
        )[:-1]
        self._append(ids, ', "parameters": {')
        params: dict[str, Any] = {}
        for index, (pname, param) in enumerate(
            self.functions[name].parameters.items()
        ):
            opening = (", " if index else "") + f'"{pname}":'
            if param.type == "string":
                opening += ' "'
            elif param.type not in ("number", "integer"):
                opening += " "
            self._append(ids, opening)
            params[pname] = self._value(ids, param.type)
        return FunctionCall(
            prompt=prompt.prompt, name=name, parameters=params
        )
