from abc import ABC, abstractmethod
from typing import Any, Union


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._content: list[str] = []
        self._count: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool: ...

    @abstractmethod
    def ingest(self, data: Any) -> None: ...

    def output(self) -> tuple[int, str]:
        if not self._content:
            raise IndexError("No data available in processor")
        rank = self._count - len(self._content)
        value = self._content.pop(0)
        return (rank, value)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, bool):
            return False
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(
                isinstance(item, (int, float)) and not isinstance(item, bool)
                for item in data
            )
        return False

    def ingest(
        self,
        data: Union[int, float, list[int], list[float], list[int | float]],
    ) -> None:
        if not self.validate(data):
            raise TypeError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                self._content.append(str(item))
                self._count += 1
        else:
            self._content.append(str(data))
            self._count += 1


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)
        return False

    def ingest(self, data: Union[str, list[str]]) -> None:
        if not self.validate(data):
            raise TypeError("Improper text data")
        if isinstance(data, list):
            for item in data:
                self._content.append(item)
                self._count += 1
        else:
            self._content.append(data)
            self._count += 1


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return all(
                isinstance(k, str) and isinstance(v, str)
                for k, v in data.items()
            )
        if isinstance(data, list):
            return all(
                isinstance(item, dict) and all(
                    isinstance(k, str) and isinstance(v, str)
                    for k, v in item.items()
                )
                for item in data
            )
        return False

    def ingest(
        self,
        data: Union[dict[str, str], list[dict[str, str]]]
    ) -> None:
        if not self.validate(data):
            raise TypeError("Improper log data")
        if isinstance(data, list):
            for item in data:
                self._content.append(
                    f"{item.get('log_level', '')}: "
                    f"{item.get('log_message', '')}"
                )
                self._count += 1
        else:
            self._content.append(
                f"{data.get('log_level', '')}: "
                f"{data.get('log_message', '')}"
            )
            self._count += 1


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            handled = False
            for proc in self._processors:
                if proc.validate(element):
                    proc.ingest(element)
                    handled = True
                    break
            if not handled:
                print(
                    f"DataStream error - Can't process element in stream: "
                    f"{element}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            name = type(proc).__name__
            total = proc._count
            remaining = len(proc._content)
            print(
                f"{name}: total {total} items processed, "
                f"remaining {remaining} on processor"
            )


def main() -> None:
    print("=== Code Nexus - Data Stream ===")
    print("\nInitialize Data Stream...")

    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Numeric Processor")
    num_proc = NumericProcessor()
    stream.register_processor(num_proc)

    batch: list[Any] = [
        'Hello world',
        [3.14, -1, 2.71],
        [
            {
                'log_level': 'WARNING',
                'log_message': 'Telnet access! Use ssh instead'
            },
            {'log_level': 'INFO', 'log_message': 'User wil is connected'}
        ],
        42,
        ['Hi', 'five']
    ]
    print(f"Send first batch of data on stream: {batch}")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("\nRegistering other data processors")
    txt_proc = TextProcessor()
    log_proc = LogProcessor()
    stream.register_processor(txt_proc)
    stream.register_processor(log_proc)

    print("Send the same batch again")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print(
        "\nConsume some elements from the data processors: "
        "Numeric 3, Text 2, Log 1"
    )
    for _ in range(3):
        num_proc.output()
    for _ in range(2):
        txt_proc.output()
    log_proc.output()
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
