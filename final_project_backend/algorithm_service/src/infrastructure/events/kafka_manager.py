import json
import threading
from typing import Callable
from kafka import KafkaProducer, KafkaConsumer
import logging

from src.globals.consts.consts_strings import ConstsStrings
from src.infrastructure.interfaces.infrastructures.ikafka_manager import IKafkaManager
from src.infrastructure.interfaces.infrastructures.iconfig_manager import IConfigManager
from src.infrastructure.factories.logger_factory import LoggerFactory
from src.globals.consts.logger_messages import LoggerMessages


class KafkaManager(IKafkaManager):
    def __init__(self, config_manager: IConfigManager) -> None:
        self._topic = None
        self._producer = None
        self._consumer = None
        self._bootstrap_servers = None
        self._config_manager = config_manager
        self._logger = LoggerFactory.get_logger_manager()
        self._init_data_from_configuration()
        self._init_kafka_producer()

    def send_message(self, topic: str, msg: str) -> None:
            if self._config_manager.exists(topic):
                self._producer.send(topic, value=msg)
                self._producer.flush()

    def start_consuming(self, topic: str, callback: Callable) -> None:
        self._init_kafka_consumer(topic)
        if self._consumer:
            thread = threading.Thread(target=self._consume, args=(callback,))
            thread.daemon = True
            thread.start()
            
    def _init_data_from_configuration(self) -> None:
        self._bootstrap_servers = self._config_manager.get(
            ConstsStrings.KAFKA_ROOT_CONFIGURATION_NAME,
            ConstsStrings.BOOTSTRAP_SERVERS_ROOT
        )

    def _init_kafka_producer(self) -> None:
        self._producer = KafkaProducer(
            bootstrap_servers=self._bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode(ConstsStrings.ENCODER)
        )

    def _init_kafka_consumer(self, topic: str) -> None:
        if not self._config_manager.exists(topic):
            self._logger.log(ConstsStrings.LOG_NAME_ERROR,
                             LoggerMessages.TOPIC_NOT_EXIST, level=logging.ERROR) 
            return
        self._consumer = KafkaConsumer(
            topic,
            bootstrap_servers=self._bootstrap_servers,
            auto_offset_reset=ConstsStrings.AUTO_OFFSET_RESET,
            enable_auto_commit=True,
            group_id=ConstsStrings.GROUP_ID,
            value_deserializer=lambda m: json.loads(m.decode(ConstsStrings.ENCODER))
        )

    def _consume(self, callback: Callable) -> None:
        for message in self._consumer:
            self._consumer.commit()
            callback(message.value)
