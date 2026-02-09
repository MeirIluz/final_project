from typing import Any
import numpy as np
import cv2
import threading

from src.globals.consts.consts_strings import ConstsStrings
from src.globals.maps.maps import Maps
from src.infrastructure.interfaces.dal.ivideo_utils import IVideoUtils


class DrawOnVideoUtil(IVideoUtils):
    lock = threading.Lock()
    counts = None  
    objects = None
    peaks = None
    frame = None

    @staticmethod
    def draw_pose(data: tuple, topology: np.ndarray) -> np.ndarray:
        with DrawOnVideoUtil.lock:
            attribute_map = Maps.data_field_to_internal_variable
            model_results = data[1].get(ConstsStrings.model_results_key, {})
            for topic, data_ in model_results.items():
                if topic in attribute_map:
                    # print("topic", topic, "data", data_)
                    setattr(DrawOnVideoUtil, attribute_map[topic], data_)
        print("frame in draw", DrawOnVideoUtil.frame)
        return DrawOnVideoUtil._draw_pose_on_frame(topology)

    @staticmethod
    def _draw_pose_on_frame(topology: np.ndarray) -> np.ndarray:
        if not DrawOnVideoUtil._is_data_available():
            return DrawOnVideoUtil.frame
        height, width = DrawOnVideoUtil.frame.shape[:2]
        num_keypoints = topology.shape[0]
        num_objects = int(DrawOnVideoUtil.counts[0])
        for i in range(num_objects):
            obj = DrawOnVideoUtil.objects[0][i]
            DrawOnVideoUtil._draw_keypoints(obj, height, width)
            DrawOnVideoUtil._draw_connections(obj, height, width, num_keypoints, topology)
        return DrawOnVideoUtil.frame

    @staticmethod
    def _is_data_available() -> bool:
        return DrawOnVideoUtil.counts is not None and DrawOnVideoUtil.objects is not None and DrawOnVideoUtil.peaks is not None
   
    @staticmethod
    def _draw_keypoints(obj: int, height: int, width: int) -> None:
        color = (0, 255, 0)  # Green color for keypoints
        num_detected_keypoints = obj.shape[0]
        for j in range(num_detected_keypoints):
            k = int(obj[j])
            if k >= 0:
                peak = DrawOnVideoUtil.peaks[0][j][k]
                x, y = DrawOnVideoUtil._get_coordinates(peak, height, width)
                cv2.circle(DrawOnVideoUtil.frame, (x, y), 3, color, 5)

    @staticmethod
    def _draw_connections(obj: int, height: int, width: int, num_keypoints: int, topology: np.ndarray) -> None:
        color = (0, 255, 0)  # Green color for connections
        for k in range(num_keypoints):
            first_keypoint, second_keypoint = topology[k][2], topology[k][3]
            if obj[first_keypoint] >= 0 and obj[second_keypoint] >= 0:
                peak0 = DrawOnVideoUtil.peaks[0][first_keypoint][obj[first_keypoint]]
                peak1 = DrawOnVideoUtil.peaks[0][second_keypoint][obj[second_keypoint]]
                start_coords = DrawOnVideoUtil._get_coordinates(peak0, height, width)
                end_coords = DrawOnVideoUtil._get_coordinates(peak1, height, width)
                cv2.line(DrawOnVideoUtil.frame, start_coords, end_coords, color, 2)

    @staticmethod
    def _get_coordinates(peak: Any, height: int, width: int) -> tuple:
        x = round(float(peak[1]) * width)
        y = round(float(peak[0]) * height)
        return x, y
