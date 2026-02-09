import os

from src.infrastructure.interfaces.handlers.ivideo_stream_handler import IVideoStreamHandler
from src.models.handlers.video_stream_handler import VideoStreamHandler
from src.models.data_classes.camera_configuration import CameraConfiguration


class HandlerFactory:
    @staticmethod
    def create_video_stream_handler(camera_config: CameraConfiguration) -> IVideoStreamHandler:
        return VideoStreamHandler(camera_config)
