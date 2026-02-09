from abc import ABC, abstractmethod
from typing import Tuple
import numpy as np


class IMovementDetection(ABC):
    """Interface for movement detection algorithm."""

    @abstractmethod
    def detect_movement(self, frame: np.ndarray) -> Tuple[np.ndarray, bool, float]:
        """
        Detect movement in a video frame.

        Args:
            frame: Input frame as numpy array

        Returns:
            Tuple containing:
                - Processed frame with movement visualization
                - Boolean indicating if movement was detected
                - Movement percentage (0.0 to 100.0)
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset the algorithm state."""
        pass

    @abstractmethod
    def set_sensitivity(self, sensitivity: float) -> None:
        """
        Set the movement detection sensitivity.

        Args:
            sensitivity: Sensitivity value (0.0 to 1.0)
        """
        pass
