from abc import ABC, abstractmethod
import numpy as np


class IPoseEstimation(ABC):
    @abstractmethod
    def get_topology(self) -> np.ndarray:
        pass
    
    @abstractmethod
    def execute(self, frame: np.ndarray) -> tuple:
        pass
