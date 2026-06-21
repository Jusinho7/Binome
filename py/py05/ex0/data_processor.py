#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any, Union, cast


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
                isinstance(item, dict)
                and all(
                    isinstance(k, str) and isinstance(v, str)
                    for k, v in item.items()
                )
                for item in data
            )
        return False

    def ingest(self,
               data: Union[dict[str, str], list[dict[str, str]]]) -> None:
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
                f"{data.get('log_level', '')}: {data.get('log_message', '')}"
            )
            self._count += 1


def main() -> None:
    print("=== Code Nexus - Data Processor ===")

    print("\nTesting Numeric Processor...")
    num_proc = NumericProcessor()

    print(f" Trying to validate input '42': {num_proc.validate(42)}")
    print(f" Trying to validate input 'Hello': {num_proc.validate('Hello')}")

    print(" Test invalid ingestion of string 'foo' without prior validation:")
    try:
        num_proc.ingest(cast(Any, "foo"))
    except TypeError as e:
        print(f" Got exception: {e}")

    data_num = [1, 2, 3, 4, 5]
    print(f" Processing data: {data_num}")
    num_proc.ingest(data_num)
    print(" Extracting 3 values...")
    for _ in range(3):
        rank, value = num_proc.output()
        print(f" Numeric value {rank}: {value}")

    print("\nTesting Text Processor...")
    txt_proc = TextProcessor()

    print(f" Trying to validate input '42': {txt_proc.validate(42)}")

    data_txt = ["Hello", "Nexus", "World"]
    print(f" Processing data: {data_txt}")
    txt_proc.ingest(data_txt)
    print(" Extracting 1 value...")
    rank, value = txt_proc.output()
    print(f" Text value {rank}: {value}")

    print("\nTesting Log Processor...")
    log_proc = LogProcessor()

    print(f" Trying to validate input 'Hello': {log_proc.validate('Hello')}")

    data_log = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f" Processing data: {data_log}")
    log_proc.ingest(data_log)
    print(" Extracting 2 values...")
    for _ in range(2):
        rank, value = log_proc.output()
        print(f" Log entry {rank}: {value}")


if __name__ == "__main__":
    main()
