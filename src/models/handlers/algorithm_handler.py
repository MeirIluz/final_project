import numpy as np
import cv2
cv2.startWindowThread()
from typing import Any, Optional

from src.globals.consts.consts_strings import ConstsStrings
from src.infrastructure.events.events import Events
from src.infrastructure.interfaces.algorithm.idepth_estimation import IDepthEstimation
from src.infrastructure.interfaces.algorithm.ipose_estimation import IPoseEstimation
from src.infrastructure.interfaces.algorithm.itrt_pose_model import ITrtPose
from src.infrastructure.interfaces.handlers.ialgorithm_handler import IAlgorithmHandler
from src.infrastructure.utils.draw_pose_on_video_util import DrawOnVideoUtil
from src.infrastructure.interfaces.dal.ievent_manager import IEventManager


class AlgorithmHandler(IAlgorithmHandler):
    def __init__(self, event_manager: IEventManager, trt_model: ITrtPose, pose_estimation: IPoseEstimation, depth_estimation: IDepthEstimation) -> None:
        self._event_manager = event_manager
        self._trt_model = trt_model
        self._pose_estimation = pose_estimation
        self._depth_estimation = depth_estimation
        self._pose_draw_frame = None
        
    def process_frame(self, frame: Any) -> Optional[np.ndarray]:
        try:
            cv2.imshow("bla bla bla", frame)
            frame = cv2.resize(frame, (680, 480))
            data_from_model = self._depth_estimation.execute(frame)
            # false none none why?
            # print("data_from_model", data_from_model)
            #! Possible error - data_from_model[0] is True when data_from_model is (False, None, None)
            if data_from_model[0] and data_from_model[0].get("state"):
                self._event_manager.emit(
                    Events.update_buzzer_state_event,
                    data=data_from_model
                )
                self._pose_draw_frame = DrawOnVideoUtil.draw_pose(data_from_model, self._pose_estimation.get_topology())
                print("_pose_draw_frame", self._pose_draw_frame)
                self._posed_frame = self._pose_draw_frame
            else:
                self._posed_frame = frame
            return self._posed_frame
        except Exception as e:
            print(f"Could not process frame for depth estimation: {e}")
            #? I added this return because after BUG2 occured nothing was returned #? Ayala
            self._posed_frame = frame #? Ayala
            return self._posed_frame #? Ayala

    