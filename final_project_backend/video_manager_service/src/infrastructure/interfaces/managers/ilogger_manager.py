from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class ILoggerManager(ABC):

    @abstractmethod
    def log(self, log_name: str, msg: str, level: Any) -> None:
        pass
