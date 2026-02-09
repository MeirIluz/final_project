from datetime import datetime
import logging
import os
import time
import cv2
from typing import Any
from src.globals.consts.consts_strings import ConstsStrings
from src.globals.consts.consts import Consts
from src.infrastructure.interfaces.handlers.ishared_memory_pipeline_handler import ISharedMemoryPipelineHandler
from src.globals.consts.logger_messages import LoggerMessages
from src.infrastructure.factories.logger_factory import LoggerFactory


class SharedMemoryPipelineHandlerTest(ISharedMemoryPipelineHandler):
    def __init__(self, video_data: Any) -> None:
        self._logger = LoggerFactory.get_logger_manager()
        self._logger.log(ConstsStrings.LOG_NAME_DEBUG,
                             LoggerMessages.IN_SHM, level=logging.DEBUG) 
        self._start_time = time.time()
        self._camera_name = video_data.get(ConstsStrings.CAMERA_NAME_KEY)
        self._camera_port = video_data.get(ConstsStrings.CAMERA_PORT_KEY)
        self._camera_ip = video_data.get(ConstsStrings.CAMERA_IP_KEY)
        self._current_writer_path = self._generate_video_path()
        os.makedirs("./recordings", exist_ok=True)
        # ? read from camera
        self._test_pipeline = f"rtspsrc location=rtsp://admin:Rd123456@{self._camera_ip}:{self._camera_port}/h264 latency=10 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink drop=true sync=false"
        self._cap = cv2.VideoCapture(self._test_pipeline, cv2.CAP_GSTREAMER)
        # ? read from video
        # video_path = "/src/videos/video0.mp4"
        # self._cap = cv2.VideoCapture(video_path)
        for i in range(Consts.SECONDS_TO_OPEN_PIPELINE):
            if self._cap.isOpened():
                self._logger.log(ConstsStrings.LOG_NAME_DEBUG,
                             LoggerMessages.CAPTURE_OPEN_SUCCESSFULLY, level=logging.DEBUG) 
                break
            self._logger.log(ConstsStrings.LOG_NAME_WARNING,
                             LoggerMessages.ATTEMPT_NOT_OPEN_YET.format(i+1), level=logging.WARNING) 
            time.sleep(Consts.MILLISECONDS_FOR_OPEN_CAP)
        else:
            self._logger.log(ConstsStrings.LOG_NAME_ERROR,
                             LoggerMessages.FAIL_TO_OPEN_CAPTURE_AFTER_5_SECONDS, level=logging.ERROR)
        self._init_writer()

    def _generate_video_path(self) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return f"./recordings/output_{timestamp}.mp4"

    def read_frame(self) -> Any:
        ret, frame = self._cap.read()
        return frame if ret else None

    def write_frame(self, frame: Any) -> None:
        if frame is None:
            return

        elapsed = time.time() - self._start_time
        if elapsed >= 10:
            self._rotate_writer()

        if self._writer.isOpened():
            self._writer.write(frame)
        else:
            self._logger.log(ConstsStrings.LOG_NAME_ERROR,
                        LoggerMessages.FRAME_NOT_WRITE, level=logging.ERROR) 

    def _init_writer(self) -> None:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self._writer = cv2.VideoWriter(
            self._current_writer_path,
            fourcc,
            Consts.VIDEO_FPS,
            Consts.VIDEO_FRAME_SIZE,
        )

    def _rotate_writer(self) -> None:
        if self._writer and self._writer.isOpened():
            self._writer.release()
        self._start_time = time.time()
        self._current_writer_path = self._generate_video_path()
        self._init_writer()

    def release(self) -> None:
        if self._cap.isOpened():
            self._cap.release()
