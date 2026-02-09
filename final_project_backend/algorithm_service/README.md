# Movement Detection Algorithm Service

This service provides real-time movement detection for video streams using computer vision techniques.

## Features

- **Real-time Movement Detection**: Uses background subtraction (MOG2) to detect moving objects
- **Visual Feedback**: Draws bounding boxes and contours around detected movement
- **Statistics Tracking**: Monitors movement percentage, frame counts, and detection rates per camera
- **Configurable Sensitivity**: Adjustable detection sensitivity (0.0 to 1.0)
- **Multi-camera Support**: Process multiple video streams simultaneously

## Algorithm Details

The movement detection algorithm uses:

- **Background Subtraction**: OpenCV's MOG2 algorithm for adaptive background modeling
- **Morphological Operations**: Noise reduction and shape refinement
- **Contour Detection**: Identifies connected regions of movement
- **Area Filtering**: Configurable minimum area threshold to ignore small movements

## Installation

### Prerequisites

- Python 3.8+
- OpenCV with contrib modules
- NumPy

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python main.py
```

### With Custom Sensitivity

```bash
export ALGORITHM_SENSITIVITY=0.7
python main.py
```

### Sensitivity Levels

- `0.0`: Least sensitive (only detects large movements)
- `0.5`: Medium sensitivity (default)
- `1.0`: Most sensitive (detects small movements)

## Configuration

The service reads configuration from environment variables:

- `ALGORITHM_SENSITIVITY`: Detection sensitivity (0.0 to 1.0, default: 0.5)
- `TEST_MODE`: Enable/disable test mode for FPS display
- Other configuration inherited from parent services

## Architecture

### Components

1. **IMovementDetection Interface** (`src/infrastructure/interfaces/algorithm/`)
   - Defines the movement detection contract

2. **MovementDetection Implementation** (`src/models/algorithm/`)
   - Implements background subtraction and contour detection
   - Configurable parameters for fine-tuning

3. **IAlgorithmHandler Interface** (`src/infrastructure/interfaces/handlers/`)
   - Defines frame processing and statistics management

4. **AlgorithmHandler Implementation** (`src/models/handlers/`)
   - Manages per-camera algorithm instances
   - Tracks statistics (frames processed, movement detected, etc.)

5. **AlgorithmFactory** (`src/infrastructure/factories/`)
   - Creates and configures algorithm components

6. **VideoManager Integration** (`src/models/managers/`)
   - Integrates algorithm into video processing pipeline

## Statistics

The service tracks the following statistics per camera:

- Total frames processed
- Frames with movement detected
- Current movement status
- Movement percentage (0-100%)
- Average movement percentage
- Last movement timestamp
- Movement detection ratio

## API

### Get Movement Stats

```python
stats = algorithm_handler.get_movement_stats(camera_index)
# Returns:
# {
#     'total_frames': int,
#     'frames_with_movement': int,
#     'movement_detected': bool,
#     'last_movement_percentage': float,
#     'average_movement': float,
#     'last_movement_time': timestamp,
#     'movement_ratio': float
# }
```

### Reset Algorithm

```python
algorithm_handler.reset_algorithm(camera_index)
```

### Change Sensitivity

```python
movement_detection.set_sensitivity(0.7)
```

## Output Visualization

Processed frames include:

- Green bounding boxes around detected movement
- Yellow contours outlining moving objects
- Status text: "MOVEMENT DETECTED" or "No Movement"
- Movement percentage display
- Number of detected objects
- Area labels for each detected object

## Performance

- Processes video at real-time speeds (depends on resolution and hardware)
- Adaptive background model improves over time
- Efficient contour detection with area filtering
- Thread-safe multi-camera processing

## Troubleshooting

### High false positive rate

- Decrease sensitivity: `ALGORITHM_SENSITIVITY=0.3`
- Increase minimum area threshold in algorithm parameters

### Missing movement detection

- Increase sensitivity: `ALGORITHM_SENSITIVITY=0.8`
- Ensure adequate lighting and contrast
- Reset algorithm if background changed: `algorithm_handler.reset_algorithm(camera_index)`

### Performance issues

- Reduce video resolution
- Increase minimum area threshold
- Process fewer cameras simultaneously

## Future Enhancements

- Object tracking (ID assignment across frames)
- Motion vectors and trajectory analysis
- Deep learning-based detection
- Alert system for specific movement patterns
- Cloud storage integration for detected events
