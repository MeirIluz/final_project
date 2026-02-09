from typing import Callable, Dict, List

from src.infrastructure.interfaces.dal.ievent_manager import IEventManager


class EventManager(IEventManager):
    def __init__(self) -> None:
        self._listeners: Dict[str, List[Callable]] = {}

    def register_event(self, event_name: str, listener: Callable) -> None:
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(listener)

    def emit(self, event_name: str, *args, **kwargs) -> None:
        if event_name in self._listeners:
            for listener in self._listeners[event_name]:
                listener(*args, **kwargs)
