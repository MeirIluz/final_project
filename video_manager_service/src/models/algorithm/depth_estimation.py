import math
from typing import Any
import numpy as np
from datetime import datetime
from src.infrastructure.factories.logger_factory import LoggerFactory
from src.globals.utils.utils import Utils
from src.test_modules.debug_csv_logger import DebugCSVLogger
from src.globals.consts.consts import Consts
from src.globals.consts.consts_strings import ConstsStrings
from src.models.data_classes.zmq_request import ZMQRequest
from src.globals.enums.response_status import ResponseStatus
from src.globals.maps.maps import Maps
from src.infrastructure.interfaces.algorithm.idepth_estimation import IDepthEstimation
from src.models.data_classes.point import Point
from src.infrastructure.interfaces.infrastructures.izmq_client_manager import IZMQClientManager


class DepthEstimation(IDepthEstimation):
    def __init__(self, zmq_client_handler: IZMQClientManager) -> None:
        self._active_child_distance = Utils.get_bool_env_var(
            ConstsStrings.ACTIVE_CHILD_DISTANCE)
        self._test_mode = Utils.get_bool_env_var(ConstsStrings.TEST_MODE_ENV)
        self._logger = LoggerFactory.get_logger_manager()
        timestamp = datetime.now().strftime(ConstsStrings.DATE_AND_TIME_FORMAT)
        self._debug_logger = DebugCSVLogger(
            ConstsStrings.CSV_FILE_NAME.format(timestamp))
        self._zmq_client_handler = zmq_client_handler
        self._keypoints = [None] * self._get_num_of_cameras()
        self._detection_state = False
        self._distances_from_camera = []
        self._distances_from_camera_child = []
        self._pixels_lengths_of_body_parts = {}
        self._real_distances = []
        self._body_part_lengths_statistically = Maps.BODY_PART_LENGTHS_STATISTICALLY
        self._body_part_name_to_indexes = Maps.BODY_PART_NAME_TO_INDEXES
        self._keypoint_index_to_name = Maps.KEYPOINT_INDEX_TO_NAME
        self._min_distance_threshold = Consts.MIN_DISTANCE_THRESHOLD
        self._avg_distance_threshold = Consts.AVG_DISTANCE_THRESHOLD

    def execute(self, frame: np.ndarray, camera_index: int) -> dict:
        if self._test_mode:
            self._debug_logger.start_frame()
        # Pose estimation removed - implement your own pose detection here
        before_valid_people = []
        valid_people = []
        for person in before_valid_people or []:
            has_good_confidence = any(
                kp is not None and kp.get(
                    ConstsStrings.CONFIDENCE_KEY, Consts.DEFAULT_JOINT_CONFIDENCE) > Consts.MIN_CONFIDENCE_THRESHOLD
                for kp in person.values()
            )
            if has_good_confidence:
                valid_people.append(person)
        self._keypoints[camera_index] = valid_people
        self._detection_state = False
        found_valid_person = False
        for person_keypoints in self._keypoints[camera_index]:
            self._process_keypoints(person_keypoints)
            if self._execute_detection_state_for_person():
                found_valid_person = True
                break
            self._reset_lists_and_dicts()
        if found_valid_person:
            self._detection_state = True
        if self._test_mode:
            self._debug_logger.end_frame()
        return self._prepare_results(frame, camera_index)

    def _get_num_of_cameras(self) -> Any:
        request = ZMQRequest(
            resource=ConstsStrings.CONFIG_RESOURCE,
            operation=ConstsStrings.GET_DATA_OPERATION,
            data={ConstsStrings.KEY_KEY: ConstsStrings.CAMERAS_KEY},
        )
        response = self._zmq_client_handler.send_request(request)
        if response.status == ResponseStatus.SUCCESS:
            cameras_array = response.data[ConstsStrings.CAMERAS_KEY]
            processed_cameras_array = [
                data for data in cameras_array
                if data.get(ConstsStrings.PROCESS_VIDEO_KEY)
            ]
            return len(processed_cameras_array)
        else:
            self._logger.log(ConstsStrings.LOG_NAME_ERROR,
                             response.data[ConstsStrings.ERROR_MESSAGE])
            raise ValueError('failed fetching cameras data')

    def _prepare_results(self, frame: np.ndarray, camera_index: int) -> dict:
        return {
            ConstsStrings.DETECTION_STATE_KEY: self._detection_state,
            ConstsStrings.FRAME_KEY: frame,
            ConstsStrings.KEYPOINTS_KEY: self._keypoints[camera_index]
        }

    def _process_keypoints(self, person_keypoints: dict) -> None:
        for body_part, (i, j) in self._body_part_name_to_indexes.items():
            name1 = self._keypoint_index_to_name.get(i)
            name2 = self._keypoint_index_to_name.get(j)
            point1 = person_keypoints.get(name1)
            point2 = person_keypoints.get(name2)
            if point1 and point2:
                p1 = Point(point1[ConstsStrings.X_POINT_KEY],
                           point1[ConstsStrings.Y_POINT_KEY])
                p2 = Point(point2[ConstsStrings.X_POINT_KEY],
                           point2[ConstsStrings.Y_POINT_KEY])
                self._calculate_pixels_length(p1, p2, body_part)

    def _calculate_pixels_length(self, p1: Point, p2: Point, body_part_name: str) -> None:
        length = np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)
        self._pixels_lengths_of_body_parts[body_part_name] = length

    def _execute_detection_state_for_person(self) -> bool:
        self._calculate_distance_from_camera()
        if self._active_child_distance:
            result = self._calculate_child_avg_distances()
        else:
            result = self._calculate_avg_distances()
        self._reset_lists_and_dicts()
        return result

    def _calculate_distance_from_camera(self) -> None:
        for part, length_px in self._pixels_lengths_of_body_parts.items():
            if part not in self._body_part_lengths_statistically or length_px <= 0:
                continue
            length_cm = self._body_part_lengths_statistically[part]
            distance = (length_cm / (length_px * Consts.IFOV *
                        Consts.RESIZE_FACTOR)) * Consts.DISTANCE_M_TO_MM_FACTOR
            distance_child = distance / Consts.DIVIDING_FACTOR_TO_CHILD_VALUE
            self._real_distances.append(distance)
            if self._test_mode:
                self._debug_logger.log_body_part(
                    part, distance, distance_child)
            self._distances_from_camera.append(
                1 if distance <= self._min_distance_threshold else 0)
            self._distances_from_camera_child.append(
                1 if distance_child <= self._min_distance_threshold else 0)

    def _calculate_avg_distances(self) -> bool:
        threshold = math.ceil(self._avg_distance_threshold *
                              len(self._distances_from_camera))
        if self._test_mode:
            self._debug_logger.log_summary(
                threshold, self._distances_from_camera.count(1))
        return self._distances_from_camera.count(1) >= threshold

    def _calculate_child_avg_distances(self) -> bool:
        threshold = math.ceil(self._avg_distance_threshold *
                              len(self._distances_from_camera))
        if self._test_mode:
            self._debug_logger.log_summary(
                threshold, self._distances_from_camera_child.count(1))
        return (
            self._distances_from_camera.count(1) >= threshold or
            self._distances_from_camera_child.count(1) >= threshold
        )

    def _reset_lists_and_dicts(self) -> None:
        self._pixels_lengths_of_body_parts = {}
        self._distances_from_camera = []
        self._distances_from_camera_child = []
        self._real_distances = []
        self._detection_state = False
