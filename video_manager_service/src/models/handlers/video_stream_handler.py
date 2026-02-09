import glob
import cv2
import os
import logging
from numpy import ndarray
from src.globals.enums.camera_protocol import CameraProtocol
from src.globals.consts.consts_strings import ConstsStrings
from src.globals.consts.consts import Consts
from src.models.data_classes.camera_configuration import CameraConfiguration
from src.globals.consts.logger_messages import LoggerMessages
from src.infrastructure.factories.logger_factory import LoggerFactory
from src.infrastructure.interfaces.handlers.ivideo_stream_handler import IVideoStreamHandler


class VideoStreamHandler(IVideoStreamHandler):
    def __init__(self, camera_config: CameraConfiguration):
        self._camera_config = camera_config
        self._frame_width = int(os.getenv(
            ConstsStrings.FRAME_WIDTH_KEY, Consts.DEFAULT_FRAME_WIDTH))
        self._frame_height = int(os.getenv(
            ConstsStrings.FRAME_HEIGHT_KEY, Consts.DEFAULT_FRAME_HEIGHT))
        self._frame_rate = int(os.getenv(
            ConstsStrings.FRAME_RATE_KEY, Consts.DEFAULT_FRAME_RATE))
        self._cap = None
        self._writer = None
        self._logger = LoggerFactory.get_logger_manager()

    def read_frame(self) -> ndarray:
        ret, frame = self._cap.read()
        if not ret:
            return None
        return frame

    def write_frame(self, frame: ndarray) -> None:
        if frame is None:
            return

        if self._writer.isOpened():
            self._writer.write(frame)
        else:
            self._logger.log(ConstsStrings.LOG_NAME_ERROR,
                             LoggerMessages.FRAME_NOT_WRITE, level=logging.ERROR)

    def release(self) -> None:
        if self._cap.isOpened():
            self._cap.release()
        if self._writer.isOpened():
            self._writer.release()

    def start(self) -> None:
        self._init_capture()
        self._init_writer()

    def _init_capture(self) -> None:
        video_capture_pipeline = self._construct_video_capture_pipeline()
        self._cap = cv2.VideoCapture(video_capture_pipeline, cv2.CAP_GSTREAMER)
        if not self._cap.isOpened():
            self._logger.log(ConstsStrings.LOG_NAME_ERROR,
                             LoggerMessages.VIDEO_CAPTURE_NOT_OPEN.format(self._camera_config.camera_ip), level=logging.ERROR)

    def _construct_video_capture_pipeline(self) -> str:
        match self._camera_config.camera_protocol:
            case CameraProtocol.AXIS:
                protocol_path = ConstsStrings.AXIS_PATH
            case CameraProtocol.ONVIF:
                protocol_path = ConstsStrings.ONVIF_PATH
            case _:
                self._logger.log(ConstsStrings.LOG_NAME_ERROR,
                                 f"Camera {self._camera_config.camera_id} missing protocol configuration")
                protocol_path = ConstsStrings.ONVIF_PATH

        video_pipeline_rtsp = ConstsStrings.VIDEO_PIPELINE_RTSP.format(
            camera_username=self._camera_config.camera_username,
            camera_password=self._camera_config.camera_password,
            camera_ip=self._camera_config.camera_ip,
            camera_port=self._camera_config.camera_port,
            protocol_path=protocol_path,
            frame_width=Consts.ALGO_FRAME_WIDTH,
            frame_height=Consts.ALGO_FRAME_HEIGHT,
        )
        return video_pipeline_rtsp

    def _init_writer(self) -> None:
        video_writer_pipeline = self._construct_video_writer_pipeline()
        self._writer = cv2.VideoWriter(
            video_writer_pipeline,
            Consts.VIDEO_FOURCC,
            Consts.VIDEO_FPS,
            (Consts.ALGO_FRAME_WIDTH, Consts.ALGO_FRAME_HEIGHT),
        )

    def _construct_video_writer_pipeline(self) -> str:
        shared_memory_path = ConstsStrings.SHARED_MEMORY_CAM_PATH.format(
            camera_id=self._camera_config.camera_id)
        return ConstsStrings.SHARED_MEMORY_PIPELINE.format(frame_height=Consts.ALGO_FRAME_HEIGHT,
                                                           frame_width=Consts.ALGO_FRAME_WIDTH,
                                                           frame_rate=self._frame_rate,
                                                           scaled_width=self._frame_width,
                                                           scaled_height=self._frame_height,
                                                           shared_memory_path=shared_memory_path)
