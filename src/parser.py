"""Defines Pydantic models for prompts, parameters, and functions."""
import sys

try:
    from pydantic import BaseModel
except ImportError:
    print(
        "Pydantic is not installed. "
        "Please install it using 'pip install pydantic'."
    )
    sys.exit(1)


class Prompt(BaseModel):
    """Represent a prompt with a string field."""

    prompt: str


class Parameter(BaseModel):
    """Represents a parameter with a type field."""

    type: str


class Function(BaseModel):
    """Represents a function with it's name, parameters, and return type."""

    name: str
    description: str
    parameters: dict[str, Parameter]
    returns: Parameter
