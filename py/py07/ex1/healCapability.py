from abc import ABC, abstractmethod
from typing import Any


class HealCapability(ABC):
    @abstractmethod
    def heal(self, target: Any = None) -> str: ...
