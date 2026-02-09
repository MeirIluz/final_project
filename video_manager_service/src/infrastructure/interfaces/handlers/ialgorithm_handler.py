from abc import ABC, abstractmethod
from typing import Any, Optional
import numpy as np


class IAlgorithmHandler(ABC):
    @abstractmethod
    def process_frame(self, frame: Any, camera_index: int) -> Optional[np.ndarray]:
        pass