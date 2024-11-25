from dataclasses import dataclass
from typing import List

@dataclass
class Role:
    id: str
    name: str
    displayName: str

def get_role_ids(roles: List[Role]) -> List[str]:
    return [role.id for role in roles]
