from src.readfile import FILE, FILE_2, ReadFile
from src.parser import Function, Prompt


class Cam:
    def run(self) -> None:
        prompt_data = ReadFile(FILE).read()
        if prompt_data is None:
            return None
        prompts = [Prompt(**item) for item in prompt_data]
        for prompt in prompts:
            print(prompt)

        print("\nReading second file...")
        function_data = ReadFile(FILE_2).read()
        if function_data is None:
            return None
        functions = [Function(**item) for item in function_data]
        for function in functions:
            for param_name, param in function.parameters.items():
                print(
                    f"Function: {function.name}, "
                    f"Parameter: {param_name}, "
                    f"Type: {param.type}"
                )
