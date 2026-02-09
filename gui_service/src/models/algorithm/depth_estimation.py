import json
import math
import numpy as np
import trt_pose

from src.globals.consts.consts import Consts
from src.globals.consts.consts_strings import ConstsStrings
from src.globals.maps.maps import Maps
from src.infrastructure.interfaces.algorithm.idepth_estimation import IDepthEstimation
from src.infrastructure.interfaces.algorithm.ipose_estimation import IPoseEstimation
from src.models.data_classes.point import Point
from src.models.data_classes.size_frame import SizeFrame


class DepthEstimation(IDepthEstimation):
    def __init__(self, pose_estimation_instance: IPoseEstimation) -> None:
        self._counts = None
        self._objects = None
        self._peaks = None
        self._counts_copy = None
        self._objects_copy = None
        self._peaks_copy = None
        self._state = False
        self.state_copy = 0
        self._distances_from_camera = []
        self._distances_from_camera_child = []
        self._pixels_lengths_of_body_parts = {}
        self.y_true_or_false = []
        self._body_part_lengths_statistically = Maps.body_part_lengths_statistically
        self._body_part_connections = Maps.body_part_connections
        self._min_distance_threshold = Consts.min_distance_threshold
        self._avg_distance_threshold = Consts.avg_distance_threshold
        with open( ConstsStrings.topology_depth_path, ConstsStrings.open_to_read) as f: human_depth_pose = json.load(f)
        self._topology = trt_pose.coco.coco_category_to_topology(human_depth_pose)
        self._pose_estimation_instance = pose_estimation_instance
        self._size_frame = SizeFrame(Consts.model_width_parameter, Consts.model_height_parameter)

    def execute(self, frame: np.ndarray) -> tuple:
        # print("frame", frame)
        self._counts, self._objects, self._peaks = self._pose_estimation_instance.execute(frame)
        # print("self._counts, self._objects, self._peaks", self._counts, self._objects, self._peaks)
        self._copy_model_results()
        num_objects = int(self._counts[0])
        if num_objects == 0:
            return self._prepare_results(frame)
        self._process_objects(num_objects)
        self._state = self._execute_state()
        if self._state:
            self.state_copy += 1
        if self.state_copy > 0:
            self._state = True
        self.state_copy = 0
        return self._prepare_results(frame)
    
    def _calculate_pixels_length(self, first_keypoint: Point, second_keypoint: Point, body_part: str) -> None:
        length_pixels = np.sqrt(
            (second_keypoint.x - first_keypoint.x) ** 2
            + (second_keypoint.y - first_keypoint.y) ** 2
        )
        self._pixels_lengths_of_body_parts[body_part] = length_pixels

    def _process_objects(self, num_objects: int) -> None:
        topology = self._topology
        num_keypoints = topology.shape[0]
        for i in range(num_objects):
            keypoints = self._objects[0][i]
            for k in range(num_keypoints):
                self._process_keypoints(topology, keypoints, k)

    def _process_keypoints(self, topology: np.ndarray, keypoints: np.ndarray, k: int) -> None:
        first_keypoint_from_topology = topology[k][2]
        second_keypoint_from_topology = topology[k][3]
        if self._are_keypoints_valid(keypoints, first_keypoint_from_topology, second_keypoint_from_topology):
            peak0, peak1 = self._get_keypoint_peaks(first_keypoint_from_topology, second_keypoint_from_topology, keypoints)
            first_keypoint = self._create_point_from_peak(peak0)
            second_keypoint = self._create_point_from_peak(peak1)
            self._calculate_and_store_pixel_length(first_keypoint, second_keypoint, first_keypoint_from_topology, second_keypoint_from_topology)

    def _are_keypoints_valid(self, keypoints: np.ndarray, first_keypoint: int, second_keypoint: int) -> bool:
        return keypoints[first_keypoint] >= 0 and keypoints[second_keypoint] >= 0

    def _get_keypoint_peaks(self, first_keypoint_from_topology: int, second_keypoint_from_topology: int, keypoints: np.ndarray) -> tuple:
        peak0 = self._peaks[0][first_keypoint_from_topology][keypoints[first_keypoint_from_topology]]
        peak1 = self._peaks[0][second_keypoint_from_topology][keypoints[second_keypoint_from_topology]]
        return peak0, peak1

    def _create_point_from_peak(self, peak: np.ndarray) -> Point:
        return Point(round(float(peak[1]) * self._size_frame.width), round(float(peak[0]) * self._size_frame.height))

    def _calculate_and_store_pixel_length(self, first_keypoint: Point, second_keypoint: Point, first_keypoint_from_topology: int, second_keypoint_from_topology: int) -> None:
        for (connection, body_part_name) in self._body_part_connections.items():
            connection_keys = tuple(map(int, connection))
            if connection_keys == (first_keypoint_from_topology, second_keypoint_from_topology):
                self._calculate_pixels_length(first_keypoint, second_keypoint, body_part_name)

    def _execute_state(self) -> bool:
        return self._execute()

    def _prepare_results(self, frame: np.ndarray) -> tuple:
        tmp =  [
            {ConstsStrings.state_key: self._state},
            {
                ConstsStrings.model_results_key: {
                    ConstsStrings.counts_key: self._counts_copy,
                    ConstsStrings.objects_key: self._objects_copy,
                    ConstsStrings.peaks_key: self._peaks_copy,
                    ConstsStrings.frame_key: frame,
                }
            }
        ]
        return tmp

    def _calculate_distance_from_camera(self) -> None:
        for body_part_name, body_part_pixel_length in self._pixels_lengths_of_body_parts.items():
            if body_part_name not in self._body_part_lengths_statistically:
                continue
            length_statistically = self._body_part_lengths_statistically[body_part_name]
            if body_part_pixel_length <= 0:
                continue
            distance_from_camera = (
                length_statistically / (body_part_pixel_length * Consts.Ifov * Consts.resize_factor)
            ) * 1000
            distance_from_camera_child = distance_from_camera / 1.3
            self._distances_from_camera.append(1 if distance_from_camera <= self._min_distance_threshold else 0)
            self._distances_from_camera_child.append(1 if distance_from_camera_child <= self._min_distance_threshold else 0)

    def _calculate_avg_distances(self) -> bool:
        count_of_ones = self._distances_from_camera.count(1)
        count_of_ones_child = self._distances_from_camera_child.count(1)
        if count_of_ones == 0:
            return False
        total_length = len(self._distances_from_camera)
        total_length_child = len(self._distances_from_camera_child)
        threshold_for_alarm = math.ceil(self._avg_distance_threshold * total_length)
        return count_of_ones >= threshold_for_alarm or count_of_ones_child >= threshold_for_alarm

    def _reset_lists_and_dicts(self) -> None:
        self._pixels_lengths_of_body_parts = {}
        self._distances_from_camera = []
        self.y_true_or_false = []
        self._state = False

    def _copy_model_results(self) -> None:
        self._counts_copy = self._counts
        self._objects_copy = self._objects
        self._peaks_copy = self._peaks

    def _execute(self) -> bool:
        state = False
        self._calculate_distance_from_camera()
        state = self._calculate_avg_distances()
        self._reset_lists_and_dicts()
        return state

 