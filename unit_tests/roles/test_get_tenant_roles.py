import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add two parent directories to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from wristband.exceptions import AuthorizationError, BadRequestError
from wristband.roles.get_tenant_roles import get_tenant_roles

class TestGetTenantRoles(unittest.TestCase):
    @patch('requests.get')
    def test_get_tenant_roles_success(self, mock_get):
        token = "valid_token"
        application_vanity_domain = "valid-domain"
        tenant_id = "tenant123"

        # Mocked response for pagination
        mock_roles_page_1 = {
            "items": [
                {"id": "role1", "name": "Admin", "displayName": "Administrator"},
                {"id": "role2", "name": "User", "displayName": "Standard User"},
            ],
            "startIndex": 1,
            "itemsPerPage": 2,
            "totalResults": 3
        }

        mock_roles_page_2 = {
            "items": [
                {"id": "role3", "name": "Guest", "displayName": "Guest User"}
            ],
            "startIndex": 3,
            "itemsPerPage": 1,
            "totalResults": 3
        }

        mock_response_page_1 = MagicMock()
        mock_response_page_1.status_code = 200
        mock_response_page_1.json.return_value = mock_roles_page_1

        mock_response_page_2 = MagicMock()
        mock_response_page_2.status_code = 200
        mock_response_page_2.json.return_value = mock_roles_page_2

        mock_get.side_effect = [mock_response_page_1, mock_response_page_2]

        roles = get_tenant_roles(
            token=token,
            application_vanity_domain=application_vanity_domain,
            tenant_id=tenant_id
        )

        # Adjusted assertions to account for dictionary output rather than Role objects
        self.assertEqual(len(roles), 3)  # There should be 3 roles total
        self.assertEqual(roles[0]["id"], "role1")
        self.assertEqual(roles[2]["displayName"], "Guest User")

if __name__ == '__main__':
    unittest.main()