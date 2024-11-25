import json
from dataclasses import dataclass
from typing import List
from wristband.roles.models.role import Role

@dataclass
class RolesResponse:

    totalResults: int
    startIndex: int
    itemsPerPage: int
    items: List[Role]


    @classmethod
    def from_json(cls, json_string):
        data = json.loads(json_string)
        return cls(**data)