# flake8: noqa: E501
"""Prompt construction."""
from src.parser import Function, Prompt

EXAMPLES = r"""Examples:
Request: Multiply 6 by 7
Call: {"name": "fn_multiply", "parameters": {"x": 6, "y": 7}}
Request: Replace all digits in 'a1b22' with '#'
Call: {"name": "fn_sub", "parameters": {"text": "a1b22", "pattern": "\\d+", "replacement": "#"}}
"""


def build_prompt(prompt: Prompt, functions: list[Function]) -> str:
    """Build the text the model continues from.

    Args:
        prompt: the user request.
        functions: the available functions.

    Returns:
        The prompt text, ending right before the JSON function call.
    """
    lines = ["Functions:"]
    for func in functions:
        params = ", ".join(
            f"{name}: {param.type}"
            for name, param in func.parameters.items()
        )
        lines.append(f"- {func.name}({params}): {func.description}")
    lines.append(EXAMPLES + f"Request: {prompt.prompt}")
    lines.append("Call:")
    return "\n".join(lines) + "\n"
