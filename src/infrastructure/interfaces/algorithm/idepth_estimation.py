from abc import ABC, abstractmethod
import numpy as np


class IDepthEstimation(ABC):
    @abstractmethod
    def execute(self, frame: np.ndarray) -> tuple:
        pass
