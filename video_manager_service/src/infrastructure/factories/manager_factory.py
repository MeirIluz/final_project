from src.globals.consts.consts_strings import ConstsStrings
from src.infrastructure.factories.algorithm_factory import AlgorithmFactory
from src.infrastructure.factories.infrastructure_factory import InfrastructureFactory
from src.infrastructure.factories.handler_factory import HandlerFactory
from src.infrastructure.interfaces.handlers.ialgorithm_handler import IAlgorithmHandler
from src.infrastructure.interfaces.infrastructures.izmq_client_manager import IZMQClientManager
from src.infrastructure.interfaces.managers.ivideo_manager import IVideoManager
from src.models.managers.video_manager import VideoManager


class ManagerFactory: 
    @staticmethod
    def create_video_manager(algorithm_handler: IAlgorithmHandler, zmq_client_handler: IZMQClientManager) -> IVideoManager:
        return VideoManager(algorithm_handler, zmq_client_handler)
    
    @staticmethod
    def create_all() -> None:
        zmq_client_handler = InfrastructureFactory.create_zmq_client_manager()
        zmq_client_handler.start()
        depth_estimation = AlgorithmFactory.create_all(zmq_client_handler)
        algorithm_handler = HandlerFactory.create_algorithm_handler(depth_estimation)
        video_manager = ManagerFactory.create_video_manager(algorithm_handler, zmq_client_handler)
        video_manager.start()
