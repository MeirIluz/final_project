from __future__ import annotations
from dataclasses import dataclass
import json
from typing import Dict

from src.globals.consts.consts_strings import ConstsStrings


@dataclass
class ZMQRequest:
    def __init__(self, resource: str, operation: str, data: Dict = {}) -> None:
        self.resource = resource
        self.operation = operation
        self.data = data

    def to_json(self) -> str:
        return json.dumps({
            ConstsStrings.resource_identifier: self.resource,
            ConstsStrings.operation_identifier: self.operation,
            ConstsStrings.data_identifier: self.data
        })
    
    @classmethod
    def from_json(self, json_str: str) -> ZMQRequest:
        request = json.loads(json_str)
        return self(resource=request[ConstsStrings.resource_identifier], 
                    operation=request[ConstsStrings.operation_identifier], 
                    data=request.get(ConstsStrings.data_identifier, {}))
    
    resource: str
    operation: str
    data: Dict