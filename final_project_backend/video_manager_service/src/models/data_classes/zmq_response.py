from __future__ import annotations
from dataclasses import dataclass
import json
from typing import Dict

from src.globals.enums.response_status import ResponseStatus
from src.globals.consts.consts_strings import ConstsStrings


@dataclass
class ZMQResponse:
    def __init__(self, status: ResponseStatus, data: Dict = {}) -> None:
        self.status = status
        self.data = data

    def to_json(self)->str:
        return json.dumps({
            ConstsStrings.STATUS_IDENTIFIER: self.status.name,
            ConstsStrings.DATA_IDENTIFIER: self.data
        })

    @classmethod
    def from_json(self, json_str: str) -> ZMQResponse:
        try:
            json_dict = json.loads(json_str)
            status = ResponseStatus[json_dict[ConstsStrings.STATUS_IDENTIFIER].upper()]
            data = json_dict.get(ConstsStrings.DATA_IDENTIFIER, {})
            return self(status=status, data=data)
        except KeyError as e:
            raise ValueError(f"{ConstsStrings.INVALID_STATUS_VALUE_IN_JSON} {json_dict.get(ConstsStrings.STATUS_IDENTIFIER)}") from e
        except json.JSONDecodeError as e:
            raise ValueError(ConstsStrings.INVALID_JSON_FORMAT) from e

    status: ResponseStatus
    data: Dict