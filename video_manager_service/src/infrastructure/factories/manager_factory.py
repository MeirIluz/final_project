from src.globals.consts.consts_strings import ConstsStrings
from src.infrastructure.factories.infrastructure_factory import InfrastructureFactory
from src.infrastructure.interfaces.infrastructures.izmq_client_manager import IZMQClientManager
from src.infrastructure.interfaces.managers.ivideo_manager import IVideoManager
from src.models.managers.video_manager import VideoManager


class ManagerFactory:
    @staticmethod
    def create_video_manager(zmq_client_handler: IZMQClientManager) -> IVideoManager:
        return VideoManager(zmq_client_handler)

    @staticmethod
    def create_all() -> None:
        zmq_client_handler = InfrastructureFactory.create_zmq_client_manager()
        zmq_client_handler.start()
        video_manager = ManagerFactory.create_video_manager(zmq_client_handler)
        video_manager.start()
