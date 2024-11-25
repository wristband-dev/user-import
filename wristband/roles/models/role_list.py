from typing import List
from wristband.roles.models.role import Role

class RoleList(List[Role]):
    def get_role_ids(self) -> List[str]:
        role_ids = []
        for role in self:
            if isinstance(role, dict):
                # Convert dict to Role
                role = Role(**role)
            role_ids.append(role.id)
        return role_ids