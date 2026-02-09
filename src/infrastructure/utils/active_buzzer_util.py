from typing import Any

from src.globals.consts.consts_strings import ConstsStrings
from src.infrastructure.events.events import Events
from src.infrastructure.interfaces.dal.iactivate_buzzer_util import IActivateBuzzerUtil
from src.infrastructure.interfaces.dal.ievent_manager import IEventManager
from src.infrastructure.interfaces.dal.ikafka_manager import IKafkaManager
from src.test_modules.debug_print import DEBUG_PRINT


class ActivateBuzzerUtil(IActivateBuzzerUtil):
    def __init__(self, event_manager: IEventManager, kafka_manager: IKafkaManager) -> None:
        self._kafka_manager = kafka_manager
        self._event_manager = event_manager
        self.buzzing = False
        self._register_events(self._event_manager)

    def _register_events(self, event_manager: IEventManager) -> None:
        event_manager.register_event(Events.update_buzzer_state_event, self._send_trigger)

    def _send_trigger(self, data: Any) -> None:
        if not self.buzzing and data is not None:
            flag = data
            if flag:
                self.buzzing = True
                DEBUG_PRINT("Buzzzzzz")
                self._kafka_manager.send_message(ConstsStrings.distance_trigger_topic_name, ConstsStrings.distance_trigger_msg)
                self.buzzing = False
