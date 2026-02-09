from typing import Dict, Tuple
import numpy as np
import time

from src.infrastructure.interfaces.handlers.ialgorithm_handler import IAlgorithmHandler
from src.infrastructure.interfaces.algorithm.imovement_detection import IMovementDetection


class AlgorithmHandler(IAlgorithmHandler):
    """
    Handler for processing video frames with movement detection algorithm.
    Manages multiple camera streams and their respective algorithm instances.
    """

    def __init__(self, movement_detection: IMovementDetection):
        """
        Initialize the algorithm handler.

        Args:
            movement_detection: Movement detection algorithm instance
        """
        self._movement_detection = movement_detection

        # Track statistics per camera
        self._camera_stats: Dict[int, dict] = {}

    def process_frame(self, frame: np.ndarray, camera_index: int) -> np.ndarray:
        """
        Process a video frame with movement detection algorithm.

        Args:
            frame: Input frame as numpy array
            camera_index: Index of the camera source

        Returns:
            Processed frame with movement detection visualization
        """
        if frame is None or frame.size == 0:
            return frame

        # Initialize stats for this camera if not exists
        if camera_index not in self._camera_stats:
            self._camera_stats[camera_index] = {
                'total_frames': 0,
                'frames_with_movement': 0,
                'last_movement_time': None,
                'last_movement_percentage': 0.0,
                'movement_detected': False,
                'average_movement': 0.0
            }

        # Process frame with movement detection
        processed_frame, movement_detected, movement_percentage = \
            self._movement_detection.detect_movement(frame)

        # Update statistics
        stats = self._camera_stats[camera_index]
        stats['total_frames'] += 1
        stats['movement_detected'] = movement_detected
        stats['last_movement_percentage'] = movement_percentage

        if movement_detected:
            stats['frames_with_movement'] += 1
            stats['last_movement_time'] = time.time()

        # Calculate average movement percentage
        if stats['total_frames'] > 0:
            stats['average_movement'] = (
                (stats['average_movement'] *
                 (stats['total_frames'] - 1) + movement_percentage)
                / stats['total_frames']
            )

        return processed_frame

    def get_movement_stats(self, camera_index: int) -> dict:
        """
        Get movement statistics for a specific camera.

        Args:
            camera_index: Index of the camera source

        Returns:
            Dictionary with movement statistics including:
                - total_frames: Total number of processed frames
                - frames_with_movement: Number of frames where movement was detected
                - movement_detected: Current movement detection status
                - last_movement_percentage: Latest movement percentage
                - average_movement: Average movement percentage across all frames
                - last_movement_time: Timestamp of last detected movement
                - movement_ratio: Ratio of frames with movement to total frames
        """
        if camera_index not in self._camera_stats:
            return {
                'total_frames': 0,
                'frames_with_movement': 0,
                'movement_detected': False,
                'last_movement_percentage': 0.0,
                'average_movement': 0.0,
                'last_movement_time': None,
                'movement_ratio': 0.0
            }

        stats = self._camera_stats[camera_index].copy()

        # Calculate movement ratio
        if stats['total_frames'] > 0:
            stats['movement_ratio'] = stats['frames_with_movement'] / \
                stats['total_frames']
        else:
            stats['movement_ratio'] = 0.0

        return stats

    def reset_algorithm(self, camera_index: int) -> None:
        """
        Reset the algorithm state for a specific camera.

        Args:
            camera_index: Index of the camera source
        """
        # Reset statistics for this camera
        if camera_index in self._camera_stats:
            self._camera_stats[camera_index] = {
                'total_frames': 0,
                'frames_with_movement': 0,
                'last_movement_time': None,
                'last_movement_percentage': 0.0,
                'movement_detected': False,
                'average_movement': 0.0
            }

        # Reset the algorithm itself
        self._movement_detection.reset()

    def get_all_camera_stats(self) -> Dict[int, dict]:
        """
        Get statistics for all cameras.

        Returns:
            Dictionary mapping camera indices to their statistics
        """
        return {
            camera_idx: self.get_movement_stats(camera_idx)
            for camera_idx in self._camera_stats.keys()
        }
