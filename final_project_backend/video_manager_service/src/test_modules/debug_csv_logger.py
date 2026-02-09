import csv
import os
from datetime import datetime

class DebugCSVLogger:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.frame_counter = 0
        self._body_parts_distances = []
        self._threshold = None
        self._num_detected = None
        self._start_timestamp = None
        self._is_detected = None

        if not os.path.exists(filepath):
            with open(filepath, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'frame_number',
                    'timestamp',
                    'body_parts_distances',
                    'threshold',
                    'num_detected_body_parts',
                    'is_detected'
                ])

    def start_frame(self):
        self._body_parts_distances = []
        self._start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self._threshold = None
        self._num_detected = None

    def log_body_part(self, body_part_name: str, distance: float, distance_child: float):
        part_string = f"{body_part_name}:{int(distance)},{int(distance_child)}"
        self._body_parts_distances.append(part_string)

    def log_summary(self, threshold: int, num_detected: int):
        self._threshold = threshold
        self._num_detected = num_detected

    def end_frame(self):
        if self._threshold and self._num_detected:
             self._is_detected = self._threshold <= self._num_detected
        else:
            self._is_detected = None
        with open(self.filepath, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                'frame_number',
                'timestamp',
                'body_parts_distances',
                'threshold',
                'num_detected_body_parts',
                'is_detected'
            ])
            writer.writerow({
                'frame_number': self.frame_counter,
                'timestamp': self._start_timestamp,
                'body_parts_distances': " ".join(self._body_parts_distances),
                'threshold': self._threshold,
                'num_detected_body_parts': self._num_detected,
                'is_detected':  self._is_detected
            })
        self.frame_counter += 1
