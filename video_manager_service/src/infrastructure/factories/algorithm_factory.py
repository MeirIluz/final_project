from src.globals.consts.consts import Consts
from src.globals.consts.consts_strings import ConstsStrings
from src.infrastructure.interfaces.algorithm.idepth_estimation import IDepthEstimation
from src.infrastructure.interfaces.infrastructures.izmq_client_manager import IZMQClientManager
from src.models.algorithm.depth_estimation import DepthEstimation


class AlgorithmFactory:
    @staticmethod
    def create_depth_estimation(zmq_client_handler: IZMQClientManager) -> IDepthEstimation:
        return DepthEstimation(zmq_client_handler)

    @staticmethod
    def create_all(zmq_client_handler: IZMQClientManager) -> None:
        depth_estimation = AlgorithmFactory.create_depth_estimation(
            zmq_client_handler)
        return depth_estimation
