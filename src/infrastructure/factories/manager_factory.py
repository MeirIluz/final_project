from src.globals.consts.consts_strings import ConstsStrings
from src.infrastructure.factories.algorithm_factory import AlgorithmFactory
from src.infrastructure.factories.infrastructure_factory import InfrastructureFactory
from src.infrastructure.factories.handler_factory import HandlerFactory
from src.infrastructure.interfaces.dal.ievent_manager import IEventManager
from src.infrastructure.interfaces.dal.ikafka_manager import IKafkaManager
from src.infrastructure.interfaces.handlers.ialgorithm_handler import IAlgorithmHandler
from src.infrastructure.interfaces.handlers.izmq_client_handler import IZMQClientHandler
from src.infrastructure.interfaces.managers.ivideo_manager import IVideoManager
from src.models.managers.video_manager import VideoManager


class ManagerFactory: 
    @staticmethod
    def create_video_manager(kafka_manager: IKafkaManager, event_manager: IEventManager, algorithm_handler: IAlgorithmHandler, zmq_client_handler: IZMQClientHandler) -> IVideoManager:
        return VideoManager(kafka_manager, event_manager, algorithm_handler, zmq_client_handler)

    @staticmethod
    def create_all() -> None:
        zmq_client_handler = HandlerFactory.create_zmq_client_handler()
        config_manager = InfrastructureFactory.create_config_manager(ConstsStrings.configuration_path)
        kafka_manager = InfrastructureFactory.create_kafka_manager(config_manager)
        event_manager = InfrastructureFactory.create_event_manager()
        trt_pose_model, pose_estimation, depth_estimation = AlgorithmFactory.create_all()
        algorithm_handler = HandlerFactory.create_algorithm_handler(event_manager, trt_pose_model, pose_estimation, depth_estimation)
        ManagerFactory.create_video_manager(kafka_manager, event_manager, algorithm_handler, zmq_client_handler)
        InfrastructureFactory.create_active_buzzer_util(event_manager, kafka_manager)