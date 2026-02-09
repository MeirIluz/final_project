from abc import ABC, abstractmethod


class ITrtPose(ABC):
    @abstractmethod
    def execute(self) -> tuple:
        pass
