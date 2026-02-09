from abc import ABC, abstractmethod
from typing import Any, Dict
import numpy as np


class IVideoUtils(ABC):
    @abstractmethod
    def draw_pose(self, data: Dict[str, Any], topology: np.ndarray) -> np.ndarray:
        pass
