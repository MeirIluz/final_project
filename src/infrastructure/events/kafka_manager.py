import json
import threading
from typing import Callable
from kafka import KafkaProducer, KafkaConsumer

from src.globals.consts.consts_strings import ConstsStrings
from src.infrastructure.interfaces.dal.ikafka_manager import IKafkaManager
from src.infrastructure.interfaces.dal.iconfig_manager import IConfigManager
from src.test_modules.debug_print import DEBUG_PRINT


class KafkaManager(IKafkaManager):
    def __init__(self, config_manager: IConfigManager) -> None:
        self._topic = None
        self._producer = None
        self._consumer = None
        self._bootstrap_servers = None
        self._config_manager = config_manager
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
            ConstsStrings.kafka_root_configuration_name,
            ConstsStrings.bootstrap_servers_root
        )

    def _init_kafka_producer(self) -> None:
        self._producer = KafkaProducer(
            bootstrap_servers=self._bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode(ConstsStrings.encoder)
        )

    def _init_kafka_consumer(self, topic: str) -> None:
        if not self._config_manager.exists(topic):
            DEBUG_PRINT("TOPIC NOT EXIST")
            return
        self._consumer = KafkaConsumer(
            topic,
            bootstrap_servers=self._bootstrap_servers,
            auto_offset_reset=ConstsStrings.auto_offset_reset,
            enable_auto_commit=True,
            group_id=ConstsStrings.group_id,
            value_deserializer=lambda m: json.loads(m.decode(ConstsStrings.encoder))
        )

    def _consume(self, callback: Callable) -> None:
        for message in self._consumer:
            self._consumer.commit()
            callback(message.value)
