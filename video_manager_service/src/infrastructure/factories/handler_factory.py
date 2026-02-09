import os

from src.infrastructure.interfaces.handlers.ivideo_stream_handler import IVideoStreamHandler
from src.infrastructure.interfaces.algorithm.idepth_estimation import IDepthEstimation
from src.infrastructure.interfaces.handlers.ialgorithm_handler import IAlgorithmHandler
from src.models.handlers.algorithm_handler import AlgorithmHandler
from src.models.handlers.video_stream_handler import VideoStreamHandler
from src.models.data_classes.camera_configuration import CameraConfiguration

class HandlerFactory:
    @staticmethod
    def create_algorithm_handler(depth_estimation: IDepthEstimation) -> IAlgorithmHandler:
        return AlgorithmHandler(depth_estimation)
    
    @staticmethod
    def create_video_stream_handler(camera_config: CameraConfiguration) -> IVideoStreamHandler:
        return VideoStreamHandler(camera_config)
