import zmq

from src.globals.enums.response_status import ResponseStatus
from src.globals.consts.consts_strings import ConstsStrings
from src.infrastructure.interfaces.handlers.izmq_client_handler import IZMQClientHandler
from src.models.data_classes.zmq_request import ZMQRequest
from src.models.data_classes.zmq_response import ZMQResponse


class ZMQClientHandler(IZMQClientHandler):
    def __init__(self, host: str, port: int) -> None:
        self._connect(host, port)

    def send_request(self, request: ZMQRequest) -> ZMQResponse:
        try:
            self._socket.send_json(request.to_json())
            response = self._socket.recv_json()
            return ZMQResponse.from_json(response)
        except Exception as e:
            return ZMQResponse(
                status=ResponseStatus.error,
                data= {ConstsStrings.error_message: str(e)}
            )

    def _connect(self, host: str, port: int) -> None:
        self.context = zmq.Context()
        self._socket = self.context.socket(zmq.REQ)
        self._socket.connect(f"{ConstsStrings.base_tcp_connection_strings}{host}:{port}")