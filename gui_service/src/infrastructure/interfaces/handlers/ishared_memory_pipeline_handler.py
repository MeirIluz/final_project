from abc import ABC, abstractmethod
from typing import Any


class ISharedMemoryPipelineHandler(ABC):
    @abstractmethod
    def read_frame(self) -> Any:
        pass

    @abstractmethod
    def write_frame(self, frame: Any) -> None:
        pass
