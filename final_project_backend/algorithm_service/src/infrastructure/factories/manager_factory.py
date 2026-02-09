from src.globals.consts.consts_strings import ConstsStrings
from src.infrastructure.factories.algorithm_factory import AlgorithmFactory
from src.infrastructure.factories.infrastructure_factory import InfrastructureFactory
from src.infrastructure.interfaces.handlers.ialgorithm_handler import IAlgorithmHandler
from src.infrastructure.interfaces.infrastructures.izmq_client_manager import IZMQClientManager
from src.infrastructure.interfaces.managers.ivideo_manager import IVideoManager
from src.models.managers.video_manager import VideoManager


class ManagerFactory:
    @staticmethod
    def create_video_manager(
        algorithm_handler: IAlgorithmHandler,
        zmq_client_handler: IZMQClientManager
    ) -> IVideoManager:
        return VideoManager(algorithm_handler, zmq_client_handler)

    @staticmethod
    def create_all(sensitivity: float = 0.5) -> None:
        zmq_client_handler = InfrastructureFactory.create_zmq_client_manager()
        zmq_client_handler.start()

        # Create algorithm handler with movement detection
        algorithm_handler = AlgorithmFactory.create_all(sensitivity)

        video_manager = ManagerFactory.create_video_manager(
            algorithm_handler, zmq_client_handler
        )
        video_manager.start()
