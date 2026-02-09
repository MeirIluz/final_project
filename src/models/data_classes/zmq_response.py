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
            ConstsStrings.status_identifier: self.status.name,
            ConstsStrings.data_identifier: self.data
        })

    @classmethod
    def from_json(self, json_str: str) -> ZMQResponse:
        try:
            json_dict = json.loads(json_str)
            status = ResponseStatus[json_dict[ConstsStrings.status_identifier].lower()]
            data = json_dict.get(ConstsStrings.data_identifier, {})
            return self(status=status, data=data)
        except KeyError as e:
            raise ValueError(f"{ConstsStrings.invalid_status_value_in_JSON} {json_dict.get(ConstsStrings.status_identifier)}") from e
        except json.JSONDecodeError as e:
            raise ValueError(ConstsStrings.invalid_JSON_format) from e

    status: ResponseStatus
    data: Dict