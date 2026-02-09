import numpy as np
import cv2
import logging

cv2.startWindowThread()
from typing import Any, Optional
from src.globals.collections.pose_collections import PoseCollections
from src.globals.consts.consts_strings import ConstsStrings
from src.globals.consts.consts import Consts
from src.infrastructure.events.events import Events
from src.infrastructure.interfaces.algorithm.idepth_estimation import IDepthEstimation
from src.infrastructure.interfaces.handlers.ialgorithm_handler import IAlgorithmHandler
from src.infrastructure.interfaces.infrastructures.ievent_manager import IEventManager
from src.infrastructure.factories.logger_factory import LoggerFactory
from src.globals.consts.logger_messages import LoggerMessages


class AlgorithmHandler(IAlgorithmHandler):
    def __init__(self, depth_estimation: IDepthEstimation) -> None:
        self._depth_estimation = depth_estimation
        self._pose_draw_frame = None
        self._logger = LoggerFactory.get_logger_manager()
        
    def process_frame(self, frame: Any, camera_index: int) -> Optional[np.ndarray]:
        try:
            data_from_model = self._depth_estimation.execute(frame,camera_index)
            if data_from_model and data_from_model.get(ConstsStrings.DETECTION_STATE_KEY):
                self._pose_draw_frame = self._draw_pose(data_from_model)
                self._posed_frame = self._pose_draw_frame
            else:
                self._posed_frame = frame
            return self._posed_frame
        except Exception as e:
            self._logger.log(ConstsStrings.LOG_NAME_ERROR,
                             LoggerMessages.FRAME_NOT_PROCESS.format(e), level=logging.ERROR) 
            self._posed_frame = frame 
            return self._posed_frame

    def _draw_pose(self, model_outputs: dict) -> np.ndarray:
        frame = model_outputs.get(ConstsStrings.FRAME_KEY)
        keypoints_list = model_outputs.get(ConstsStrings.KEYPOINTS_KEY, [])
        for person_keypoints in keypoints_list:
            if person_keypoints:
                frame = self._draw_person_skeleton(
                    frame, person_keypoints)
        return frame

    def _draw_person_skeleton(self, frame: np.ndarray, keypoints: dict) -> np.ndarray:
        color = Consts.POSE_DRAWING_COLOR
        for joint_name, point in keypoints.items():
            if point and point.get(ConstsStrings.CONFIDENCE_KEY, Consts.DEFAULT_JOINT_CONFIDENCE) > Consts.MIN_CONFIDENCE_FOR_DRAWING:
                x, y = int(point[ConstsStrings.X_POINT_KEY]), int(
                    point[ConstsStrings.Y_POINT_KEY])
                cv2.circle(frame, (x, y), Consts.JOINT_CIRCLE_RADIUS,
                           color, Consts.JOINT_CIRCLE_FILL_VALUE)
        for joint1, joint2 in PoseCollections.JOINT_NAME_PAIRS:
            p1 = keypoints.get(joint1)
            p2 = keypoints.get(joint2)
            if p1 and p2 and p1.get(ConstsStrings.CONFIDENCE_KEY, Consts.DEFAULT_JOINT_CONFIDENCE) > Consts.MIN_CONFIDENCE_FOR_DRAWING and p2.get(ConstsStrings.CONFIDENCE_KEY, Consts.DEFAULT_JOINT_CONFIDENCE) > Consts.MIN_CONFIDENCE_FOR_DRAWING:
                pt1 = (int(p1[ConstsStrings.X_POINT_KEY]),
                       int(p1[ConstsStrings.Y_POINT_KEY]))
                pt2 = (int(p2[ConstsStrings.X_POINT_KEY]),
                       int(p2[ConstsStrings.Y_POINT_KEY]))
                cv2.line(frame, pt1, pt2, color,
                         Consts.SKELETON_LINE_THICKNESS)
        return frame

