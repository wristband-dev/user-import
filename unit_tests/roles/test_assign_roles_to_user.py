import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add two parent directories to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from wristband.exceptions import BadRequestError
from wristband.roles.models.role import Role
from wristband.roles.models.role_list import RoleList
from wristband.roles.assign_roles_to_user import assign_roles_to_user

class TestAssignRolesToUser(unittest.TestCase):
    @patch('requests.post')
    def test_assign_roles_to_user_success(self, mock_post):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Roles assigned successfully"}
        mock_post.return_value = mock_response

        token = "valid_token"
        application_vanity_domain = "valid-domain"
        user_id = "12345"
        roles = [
            Role(id="role1", name="Admin", displayName="Administrator"),
            Role(id="role2", name="User", displayName="Standard User")
        ]

        # Act
        response = assign_roles_to_user(
            token=token,
            application_vanity_domain=application_vanity_domain,
            user_id=user_id,
            roles=roles
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        mock_post.assert_called_once_with(
            f'https://{application_vanity_domain}/api/v1/users/{user_id}/assign-roles',
            headers={
                'accept': 'application/json',
                'authorization': f'Bearer {token}',
                'content-type': 'application/json',
            },
            json={'roleIds': RoleList(roles).get_role_ids()}
        )

    @patch('requests.post')
    def test_assign_roles_to_user_bad_request(self, mock_post):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Bad Request"}
        mock_post.return_value = mock_response

        token = "valid_token"
        application_vanity_domain = "valid-domain"
        user_id = "12345"
        roles = [
            Role(id="role1", name="Admin", displayName="Administrator"),
            Role(id="role2", name="User", displayName="Standard User")
        ]

        # Act & Assert
        with self.assertRaises(BadRequestError):
            assign_roles_to_user(
                token=token,
                application_vanity_domain=application_vanity_domain,
                user_id=user_id,
                roles=roles
            )

    @patch('requests.post')
    def test_assign_roles_to_user_unauthorized(self, mock_post):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Unauthorized"}
        mock_post.return_value = mock_response

        token = "invalid_token"
        application_vanity_domain = "valid-domain"
        user_id = "12345"
        roles = [
            Role(id="role1", name="Admin", displayName="Administrator"),
            Role(id="role2", name="User", displayName="Standard User")
        ]

        # Act & Assert
        with self.assertRaises(BadRequestError):  # Customize if another exception is expected
            assign_roles_to_user(
                token=token,
                application_vanity_domain=application_vanity_domain,
                user_id=user_id,
                roles=roles
            )

if __name__ == '__main__':
    unittest.main()