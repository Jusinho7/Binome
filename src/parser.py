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
    prompt: str


class Parameter(BaseModel):
    type: str


class Function(BaseModel):
    name: str
    description: str
    parameters: dict[str, Parameter]
    returns: Parameter
