import os
from src.infrastructure.interfaces.infrastructures.izmq_client_manager import IZMQClientManager
from src.globals.consts.consts_strings import ConstsStrings
from src.infrastructure.events.zmq_client_manager import ZMQClientManager
from src.infrastructure.interfaces.infrastructures.ievent_manager import IEventManager
from src.infrastructure.events.kafka_manager import KafkaManager
from src.infrastructure.events.event_manager import EventManager
from src.infrastructure.config.xml_config_manager import XMLConfigManager
from src.infrastructure.interfaces.infrastructures.iconfig_manager import IConfigManager
from src.infrastructure.interfaces.infrastructures.ikafka_manager import IKafkaManager


class InfrastructureFactory:
    event_manager: IEventManager = None

    @staticmethod
    def create_config_manager(config_path: str) -> IConfigManager:
        return XMLConfigManager(config_path)
    
    @staticmethod
    def create_kafka_manager(config_manager:IConfigManager) -> IKafkaManager:
        return KafkaManager(config_manager)

    @staticmethod
    def create_event_manager() -> IEventManager:
        if InfrastructureFactory.event_manager is None:
            InfrastructureFactory.event_manager = EventManager()
        return InfrastructureFactory.event_manager
    
    @staticmethod
    def create_zmq_client_manager() -> IZMQClientManager:
        host = os.getenv(ConstsStrings.ZMQ_SERVER_HOST)
        port = os.getenv(ConstsStrings.ZMQ_SERVER_PORT)
        return ZMQClientManager(host, port)
