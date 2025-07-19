from abc import ABC, abstractmethod
from typing import Any
from .atomic_write import atomic_write

class IEventSource(ABC):
    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

class IFileWriter(ABC):
    @abstractmethod
    def write(self, path: str, content: str) -> bool:
        pass

class AtomicFileWriter(IFileWriter):
    def write(self, path: str, content: str) -> bool:
        return atomic_write(path, content) 