import os

from src.infrastructure.interfaces.dal.ievent_manager import IEventManager
from src.infrastructure.interfaces.algorithm.idepth_estimation import IDepthEstimation
from src.infrastructure.interfaces.algorithm.ipose_estimation import IPoseEstimation
from src.infrastructure.interfaces.algorithm.itrt_pose_model import ITrtPose
from src.globals.consts.consts_strings import ConstsStrings
from src.infrastructure.interfaces.handlers.ialgorithm_handler import IAlgorithmHandler
from src.infrastructure.interfaces.handlers.izmq_client_handler import IZMQClientHandler
from src.models.handlers.algorithm_handler import AlgorithmHandler
from src.models.handlers.zmq_client_handler import ZMQClientHandler


class HandlerFactory:
    @staticmethod
    def create_algorithm_handler(event_manager: IEventManager, trt_pose_model: ITrtPose, pose_estimation: IPoseEstimation, depth_estimation: IDepthEstimation) -> IAlgorithmHandler:
        return AlgorithmHandler(event_manager, trt_pose_model, pose_estimation, depth_estimation)
    
    @staticmethod
    def create_zmq_client_handler() -> IZMQClientHandler:
        host = os.getenv(ConstsStrings.zmq_server_host)
        port = os.getenv(ConstsStrings.zmq_server_port)
        return ZMQClientHandler(host, port)