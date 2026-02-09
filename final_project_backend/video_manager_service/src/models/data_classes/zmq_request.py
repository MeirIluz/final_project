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
            ConstsStrings.RESOURCE_IDENTIFIER: self.resource,
            ConstsStrings.OPERATION_IDENTIFIER: self.operation,
            ConstsStrings.DATA_IDENTIFIER: self.data
        })
    
    @classmethod
    def from_json(self, json_str: str) -> ZMQRequest:
        request = json.loads(json_str)
        return self(resource=request[ConstsStrings.RESOURCE_IDENTIFIER], 
                    operation=request[ConstsStrings.OPERATION_IDENTIFIER], 
                    data=request.get(ConstsStrings.DATA_IDENTIFIER, {}))
    
    resource: str
    operation: str
    data: Dict