from abc import ABC, abstractmethod
from typing import Tuple
import numpy as np


class IAlgorithmHandler(ABC):
    """Interface for algorithm handler that processes video frames."""

    @abstractmethod
    def process_frame(self, frame: np.ndarray, camera_index: int) -> np.ndarray:
        """
        Process a video frame with the algorithm.

        Args:
            frame: Input frame as numpy array
            camera_index: Index of the camera source

        Returns:
            Processed frame with algorithm results visualized
        """
        pass

    @abstractmethod
    def get_movement_stats(self, camera_index: int) -> dict:
        """
        Get movement statistics for a specific camera.

        Args:
            camera_index: Index of the camera source

        Returns:
            Dictionary with movement statistics
        """
        pass

    @abstractmethod
    def reset_algorithm(self, camera_index: int) -> None:
        """
        Reset the algorithm state for a specific camera.

        Args:
            camera_index: Index of the camera source
        """
        pass
