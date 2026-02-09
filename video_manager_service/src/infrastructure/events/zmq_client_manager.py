import zmq

from src.globals.enums.response_status import ResponseStatus
from src.globals.consts.consts_strings import ConstsStrings
from src.infrastructure.interfaces.infrastructures.izmq_client_manager import IZMQClientManager
from src.models.data_classes.zmq_request import ZMQRequest
from src.models.data_classes.zmq_response import ZMQResponse


class ZMQClientManager(IZMQClientManager):
    def __init__(self, host: str, port: int) -> None:
        self.context = zmq.Context()
        self._socket = self.context.socket(zmq.REQ)
        self._address = f"{ConstsStrings.BASE_TCP_CONNECTION_STRINGS}{host}:{port}"

    def start(self) -> None:
        self._socket.connect(self._address)

    def stop(self) -> None:
        self._socket.close()

    def send_request(self, request: ZMQRequest) -> ZMQResponse:
        try:
            self._socket.send_json(request.to_json())
            response = self._socket.recv_json()
            return ZMQResponse.from_json(response)
        except Exception as e:
            return ZMQResponse(
                status=ResponseStatus.ERROR,
                data={ConstsStrings.ERROR_MESSAGE: str(e)}
            )
