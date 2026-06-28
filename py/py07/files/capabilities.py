from abc import ABC, abstractmethod


class HealCapability(ABC):
    """Abstract capability for Creatures that can heal."""

    @abstractmethod
    def heal(self) -> str:
        pass


class TransformCapability(ABC):
    """Abstract capability for Creatures that can transform."""

    def __init__(self) -> None:
        self._transformed: bool = False

    @abstractmethod
    def transform(self) -> str:
        pass

    @abstractmethod
    def revert(self) -> str:
        pass
