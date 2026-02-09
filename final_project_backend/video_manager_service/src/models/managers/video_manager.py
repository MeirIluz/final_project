import collections
import os
import threading
import time
from typing import Any
import logging

import cv2
import numpy as np

from src.globals.consts.consts import Consts
from src.globals.consts.consts_strings import ConstsStrings
from src.globals.enums.response_status import ResponseStatus
from src.globals.utils.utils import Utils
from src.infrastructure.factories.handler_factory import HandlerFactory
from src.infrastructure.interfaces.infrastructures.izmq_client_manager import IZMQClientManager
from src.infrastructure.interfaces.managers.ivideo_manager import IVideoManager
from src.models.data_classes.zmq_request import ZMQRequest
from src.models.data_classes.camera_configuration import CameraConfiguration
from src.test_modules.display_video_test import DisplayVideoTest
from src.infrastructure.factories.logger_factory import LoggerFactory
from src.globals.consts.logger_messages import LoggerMessages


class VideoManager(IVideoManager):

    def __init__(self, zmq_client_handler: IZMQClientManager) -> None:
        self._test_mode = Utils.get_bool_env_var(ConstsStrings.TEST_MODE_ENV)
        self._zmq_client_handler = zmq_client_handler
        self._video_data = [
            data for data in self._get_data_from_config(ConstsStrings.CAMERAS_KEY)
            if data.get(ConstsStrings.PROCESS_VIDEO_KEY)
        ]
        self._pipelines = []
        self._num_cameras = len(self._video_data)
        self._frame_times = collections.deque(maxlen=Consts.VIDEO_FPS)
        self._start_time = time.time()
        self._frame_count = 0
        self._real_fps = Consts.REAL_FPS
        self._lock_write_posed_frames = threading.Lock()

        self._process_video_threads = []
        self._posed_frames = [None] * self._num_cameras
        if self._test_mode:
            self._display_video = DisplayVideoTest(
                ConstsStrings.IMSHOW_WINDOW_NAME)
        self._init_video_capture()
        self._logger = LoggerFactory.get_logger_manager()

    def start(self) -> None:
        for i in range(self._num_cameras):
            thread = threading.Thread(
                target=self._process_frames_for_camera, args=(i,)
            )
            self._process_video_threads.append(thread)
            thread.start()
        if self._test_mode:
            try:
                while True:
                    with self._lock_write_posed_frames:
                        self._display_video.concat_and_show_frames(
                            self._posed_frames)
                    if cv2.waitKey(1) & 0xFF == ord(ConstsStrings.EXIT_KEY_IMSHOW):
                        break
            finally:
                self.stop()

    def stop(self) -> None:
        for pipeline in self._pipelines:
            pipeline.release()
        for thread in self._process_video_threads:
            thread.join()
        if self._test_mode:
            self._display_video.close()

    def _init_video_capture(self) -> None:
        self._remove_shared_memory_files()
        for camera in self._video_data:
            camera_id = camera.get(ConstsStrings.CAMERA_ID_KEY)
            camera_ip = camera.get(ConstsStrings.CAMERA_IP_KEY)
            camera_port = camera.get(ConstsStrings.CAMERA_PORT_KEY)
            camera_username = camera.get(ConstsStrings.CAMERA_USERNAME_KEY)
            camera_password = camera.get(ConstsStrings.CAMERA_PASSWORD_KEY)
            camera_protocol = camera.get(ConstsStrings.CAMERA_PROTOCOL_KEY)
            camera_config = CameraConfiguration(
                camera_id=camera_id,
                camera_ip=camera_ip,
                camera_port=camera_port,
                camera_username=camera_username,
                camera_password=camera_password,
                camera_protocol=camera_protocol,
            )
            camera_video_handler = HandlerFactory.create_video_stream_handler(
                camera_config)
            self._pipelines.append(
                camera_video_handler)
            camera_video_handler.start()

    def _get_data_from_config(self, key: str) -> Any:
        request = ZMQRequest(
            resource=ConstsStrings.CONFIG_RESOURCE,
            operation=ConstsStrings.GET_DATA_OPERATION,
            data={ConstsStrings.KEY_KEY: key},
        )
        response = self._zmq_client_handler.send_request(request)
        if response.status == ResponseStatus.SUCCESS:
            return response.data[key]
        self._logger.log(ConstsStrings.LOG_NAME_ERROR,
                         response.data[ConstsStrings.ERROR_MESSAGE])
        raise ValueError("Failed fetching cameras data")

    def _process_frames_for_camera(self, camera_index: int) -> None:
        pipeline = self._pipelines[camera_index]
        while True:
            frame = pipeline.read_frame()
            if frame is None:
                continue
            if self._test_mode:
                self._frame_times.append(time.time())
                self._frame_count += 1
                real_fps, avg_fps = Utils.calculate_fps(
                    self._frame_times, self._frame_count, self._start_time
                )
                self._real_fps = real_fps
            with self._lock_write_posed_frames:
                self._posed_frames[camera_index] = frame
                pipeline.write_frame(frame)

    def _remove_shared_memory_files(self) -> None:
        file_prefixes = ConstsStrings.SHARED_MEMORY_FILES_PREFIXES
        files = [f for f in os.listdir(ConstsStrings.SHARED_MEMORY_PATH) if any(
            f.startswith(prefix) for prefix in file_prefixes)]
        for file in files:
            try:
                os.remove(os.path.join(ConstsStrings.SHARED_MEMORY_PATH, file))
            except Exception as e:
                self._logger.log(ConstsStrings.LOG_NAME_ERROR,
                                 LoggerMessages.SHARED_MEMORY_FILE_REMOVE_ERROR.format(file, e), level=logging.ERROR)
