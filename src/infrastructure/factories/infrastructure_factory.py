from src.infrastructure.interfaces.dal.iactivate_buzzer_util import IActivateBuzzerUtil
from src.infrastructure.interfaces.dal.ievent_manager import IEventManager
from src.infrastructure.events.kafka_manager import KafkaManager
from src.infrastructure.events.event_manager import EventManager
from src.infrastructure.config.xml_config_manager import XMLConfigManager
from src.infrastructure.interfaces.dal.iconfig_manager import IConfigManager
from src.infrastructure.interfaces.dal.ikafka_manager import IKafkaManager
from src.infrastructure.utils.active_buzzer_util import ActivateBuzzerUtil


class InfrastructureFactory:
    @staticmethod
    def create_config_manager(config_path: str) -> IConfigManager:
        return XMLConfigManager(config_path)
    
    @staticmethod
    def create_kafka_manager(config_manager:IConfigManager) -> IKafkaManager:
        return KafkaManager(config_manager)

    @staticmethod
    def create_event_manager() -> IEventManager:
        return EventManager()
    
    @staticmethod
    def create_active_buzzer_util(event_manager: IEventManager, kafka_manager: IKafkaManager) -> IActivateBuzzerUtil:
        return ActivateBuzzerUtil(event_manager, kafka_manager)
