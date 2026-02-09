from typing import Tuple, Optional
import cv2
import numpy as np

from src.infrastructure.interfaces.algorithm.imovement_detection import IMovementDetection


class MovementDetection(IMovementDetection):
    """
    Movement detection algorithm using background subtraction and frame differencing.
    Detects motion in video frames and highlights moving areas.
    """

    def __init__(
        self,
        sensitivity: float = 0.5,
        min_area: int = 500,
        blur_kernel_size: Tuple[int, int] = (21, 21),
        threshold_value: int = 25
    ):
        """
        Initialize the movement detection algorithm.

        Args:
            sensitivity: Detection sensitivity (0.0 to 1.0), higher = more sensitive
            min_area: Minimum contour area to consider as movement
            blur_kernel_size: Gaussian blur kernel size for noise reduction
            threshold_value: Threshold value for binary image (0-255)
        """
        self._sensitivity = sensitivity
        # Lower threshold for higher sensitivity
        self._min_area = int(min_area * (1.0 - sensitivity))
        self._blur_kernel_size = blur_kernel_size
        self._threshold_value = int(threshold_value * (1.0 + sensitivity))

        # Background subtractor for more advanced motion detection
        self._bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500,
            varThreshold=16,
            detectShadows=True
        )

        # Store previous frames for frame differencing
        self._prev_frame: Optional[np.ndarray] = None
        self._frame_count = 0

    def detect_movement(self, frame: np.ndarray) -> Tuple[np.ndarray, bool, float]:
        """
        Detect movement in a video frame using background subtraction.

        Args:
            frame: Input frame as numpy array (BGR format)

        Returns:
            Tuple containing:
                - Processed frame with movement visualization (contours and bounding boxes)
                - Boolean indicating if significant movement was detected
                - Movement percentage (0.0 to 100.0)
        """
        if frame is None or frame.size == 0:
            return frame, False, 0.0

        self._frame_count += 1

        # Create a copy for visualization
        output_frame = frame.copy()

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        gray_blur = cv2.GaussianBlur(gray, self._blur_kernel_size, 0)

        # Apply background subtraction
        fg_mask = self._bg_subtractor.apply(gray_blur)

        # Remove shadows (value 127) and keep only foreground (value 255)
        _, fg_mask = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)

        # Apply morphological operations to remove noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fg_mask = cv2.morphologyEx(
            fg_mask, cv2.MORPH_OPEN, kernel, iterations=2)
        fg_mask = cv2.morphologyEx(
            fg_mask, cv2.MORPH_DILATE, kernel, iterations=2)

        # Find contours of moving objects
        contours, _ = cv2.findContours(
            fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Calculate movement metrics
        movement_detected = False
        total_movement_area = 0
        frame_area = frame.shape[0] * frame.shape[1]

        # Draw contours and bounding boxes around moving objects
        for contour in contours:
            area = cv2.contourArea(contour)

            if area < self._min_area:
                continue

            movement_detected = True
            total_movement_area += area

            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)

            # Draw bounding box
            cv2.rectangle(output_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Draw contour
            cv2.drawContours(output_frame, [contour], -1, (0, 255, 255), 2)

            # Add area label
            cv2.putText(
                output_frame,
                f"Area: {int(area)}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

        # Calculate movement percentage
        movement_percentage = (total_movement_area / frame_area) * 100.0

        # Add status text to frame
        status_text = "MOVEMENT DETECTED" if movement_detected else "No Movement"
        status_color = (0, 0, 255) if movement_detected else (0, 255, 0)

        cv2.putText(
            output_frame,
            status_text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            status_color,
            2
        )

        cv2.putText(
            output_frame,
            f"Movement: {movement_percentage:.2f}%",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            output_frame,
            f"Objects: {len([c for c in contours if cv2.contourArea(c) >= self._min_area])}",
            (10, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        return output_frame, movement_detected, movement_percentage

    def reset(self) -> None:
        """Reset the algorithm state and background model."""
        self._prev_frame = None
        self._frame_count = 0
        self._bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500,
            varThreshold=16,
            detectShadows=True
        )

    def set_sensitivity(self, sensitivity: float) -> None:
        """
        Set the movement detection sensitivity.

        Args:
            sensitivity: Sensitivity value (0.0 to 1.0), higher = more sensitive
        """
        if not 0.0 <= sensitivity <= 1.0:
            raise ValueError("Sensitivity must be between 0.0 and 1.0")

        self._sensitivity = sensitivity
        # Adjust min_area inversely to sensitivity
        base_min_area = 500
        self._min_area = int(base_min_area * (1.0 - sensitivity * 0.9))

    def get_sensitivity(self) -> float:
        """Get current sensitivity value."""
        return self._sensitivity
