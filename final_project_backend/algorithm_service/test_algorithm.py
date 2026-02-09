"""
Simple test script for movement detection algorithm.
Tests the algorithm with a webcam or video file.
"""

from src.models.algorithm.movement_detection import MovementDetection
import cv2
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def test_with_webcam(sensitivity=0.5):
    """Test movement detection with webcam."""
    print("Testing Movement Detection with Webcam")
    print(f"Sensitivity: {sensitivity}")
    print("Press 'q' to quit, 'r' to reset algorithm, '+'/'-' to adjust sensitivity")
    print("-" * 60)

    # Initialize algorithm
    detector = MovementDetection(sensitivity=sensitivity)

    # Open webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error reading frame")
            break

        frame_count += 1

        # Detect movement
        processed_frame, movement_detected, movement_percentage = detector.detect_movement(
            frame)

        # Add frame info
        cv2.putText(
            processed_frame,
            f"Frame: {frame_count}",
            (10, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.putText(
            processed_frame,
            f"Sensitivity: {detector.get_sensitivity():.2f}",
            (10, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        # Display
        cv2.imshow('Movement Detection Test', processed_frame)

        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('r'):
            print("Resetting algorithm...")
            detector.reset()
            frame_count = 0
        elif key == ord('+') or key == ord('='):
            new_sens = min(1.0, detector.get_sensitivity() + 0.1)
            detector.set_sensitivity(new_sens)
            print(f"Sensitivity increased to {new_sens:.2f}")
        elif key == ord('-') or key == ord('_'):
            new_sens = max(0.0, detector.get_sensitivity() - 0.1)
            detector.set_sensitivity(new_sens)
            print(f"Sensitivity decreased to {new_sens:.2f}")

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("\nTest completed!")


def test_with_video(video_path, sensitivity=0.5):
    """Test movement detection with video file."""
    print(f"Testing Movement Detection with Video: {video_path}")
    print(f"Sensitivity: {sensitivity}")
    print("Press 'q' to quit, 'r' to reset, SPACE to pause")
    print("-" * 60)

    # Initialize algorithm
    detector = MovementDetection(sensitivity=sensitivity)

    # Open video
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video file: {video_path}")
        return

    frame_count = 0
    paused = False

    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                print("End of video")
                break

            frame_count += 1

            # Detect movement
            processed_frame, movement_detected, movement_percentage = detector.detect_movement(
                frame)

            # Add frame info
            cv2.putText(
                processed_frame,
                f"Frame: {frame_count}",
                (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

        # Display
        cv2.imshow('Movement Detection Test', processed_frame)

        # Handle keyboard input
        key = cv2.waitKey(30 if not paused else 0) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('r'):
            print("Resetting algorithm...")
            detector.reset()
        elif key == ord(' '):
            paused = not paused
            print("Paused" if paused else "Resumed")

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("\nTest completed!")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Test movement detection algorithm')
    parser.add_argument('--video', type=str,
                        help='Path to video file (use webcam if not provided)')
    parser.add_argument('--sensitivity', type=float, default=0.5,
                        help='Detection sensitivity (0.0 to 1.0)')

    args = parser.parse_args()

    if args.video:
        test_with_video(args.video, args.sensitivity)
    else:
        test_with_webcam(args.sensitivity)
