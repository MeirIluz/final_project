from abc import ABC, abstractmethod

from src.models.data_classes.zmq_request import ZMQRequest
from src.models.data_classes.zmq_response import ZMQResponse


class IZMQClientHandler(ABC):
    @abstractmethod
    def send_request(self, request: ZMQRequest) -> ZMQResponse:
        pass
