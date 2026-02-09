import threading

import numpy as np
import cv2
from typing import Any

from src.infrastructure.interfaces.handlers.ialgorithm_handler import IAlgorithmHandler
from src.infrastructure.interfaces.dal.ievent_manager import IEventManager
from src.infrastructure.interfaces.dal.ikafka_manager import IKafkaManager
from src.infrastructure.interfaces.handlers.izmq_client_handler import IZMQClientHandler
from src.infrastructure.interfaces.managers.ivideo_manager import IVideoManager
from src.models.data_classes.zmq_request import ZMQRequest
from src.globals.enums.response_status import ResponseStatus
from src.globals.consts.consts_strings import ConstsStrings
from src.models.handlers.shared_memory_pipeline_handler import SharedMemoryPipelineHandler


class VideoManager(IVideoManager):
    lock = threading.Lock()

    def __init__(self, kafka_manager: IKafkaManager, event_manager: IEventManager, algorithm_handler: IAlgorithmHandler, zmq_client_handler: IZMQClientHandler) -> None:
        self._kafka_manager = kafka_manager
        self._event_manager = event_manager
        self._algorithm_handler = algorithm_handler
        self._zmq_client_handler = zmq_client_handler
        self._video_data = self._get_data_from_config(ConstsStrings.cameras_key)
        # self._num_cameras = len(self._video_data)
        self._num_cameras = 1
        self._pipelines = [
            SharedMemoryPipelineHandler(self._video_data[i].get("camera_name"))
            for i in range(self._num_cameras)
        ]
        self._posed_frames = [None] * self._num_cameras
        self._run()
    
    def _run(self) -> None:
        threads = []
        for i in range(self._num_cameras):
            thread = threading.Thread(target=self._process_frames_for_camera, args=(i,))
            threads.append(thread)
            thread.start()
        while True:
            display_response = self._concat_and_show_frames()
            if display_response == 'q':
                print("Stopping Software")
                cv2.destroyAllWindows()
                break
        for thread in threads:
            thread.join()

    def _get_data_from_config(self, key: str) -> Any:
        request = ZMQRequest(
            resource=ConstsStrings.config_resource,
            operation=ConstsStrings.get_data_operation,
            data={ConstsStrings.key_key: key},
        )
        response = self._zmq_client_handler.send_request(request)
        if response.status == ResponseStatus.success:
            return response.data[key]
        return None

    def _process_frames_for_camera(self, camera_index: int) -> None:
        pipeline = self._pipelines[camera_index]
        while True:
            print("in while")
            frame = pipeline.read_frame() 
            if frame is None:
                print("frame is none +++++++++")
                continue
            print("frame is not none", frame)
            processed_frame = self._algorithm_handler.process_frame(frame)
            print("processed_frame", processed_frame)
            #! BUG3: processed_frame returned from algorithm is always None (caused by BUG2)
            print("before lock")
            with self.lock:
                self._posed_frames[camera_index] = processed_frame
                # pipeline.write_frame(processed_frame) # using shm
            print("after lock")

    def _concat_and_show_frames(self) -> str:
        with self.lock:
            frames = []
            for frame in self._posed_frames:
                if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
                    # print("frame inn")
                    resized_frame = cv2.resize(frame, (640, 480))  # התאמה לגודל אחיד
                else:
                    resized_frame = np.zeros((480, 640, 3), dtype=np.uint8)  # מסגרת שחורה
                frames.append(resized_frame)

            # הדפסת מידע לבדיקה
            # print(f"Number of frames: {len(frames)}")
            # for i, f in enumerate(frames):
            #     print(f"Frame {i}: shape={f.shape}, dtype={f.dtype}")

            # בדיקה שכל הפריימים בגודל זהה ובאותו סוג נתונים
            first_shape = frames[0].shape
            first_dtype = frames[0].dtype
            valid_frames = [f for f in frames if f.shape == first_shape and f.dtype == first_dtype]

            if len(valid_frames) > 0:
                combined_frame = cv2.hconcat(valid_frames)
            else:
                combined_frame = np.zeros((480, 640 * len(frames), 3), dtype=np.uint8)  # מסגרת שחורה גדולה

            cv2.imshow("Processed Frames", combined_frame)
            return cv2.waitKey(1) & 0xFF
