import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add two parent directories to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from wristband.exceptions import BadRequestError, AuthorizationError
from wristband.users.invite_existing_user import invite_existing_user

class TestInviteExistingUser(unittest.TestCase):
    @patch('requests.post')
    def test_invite_existing_user_success(self, mock_post):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "User invited successfully"}
        mock_post.return_value = mock_response

        token = "valid_token"
        application_vanity_domain = "valid-domain"
        tenant_id = "tenant123"
        identity_provider_name = "idpName"
        user_id = "userXYZ"

        # Act
        response = invite_existing_user(
            token=token,
            application_vanity_domain=application_vanity_domain,
            tenant_id=tenant_id,
            identity_provider_name=identity_provider_name,
            user_id=user_id
        )

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "User invited successfully"})
        mock_post.assert_called_once_with(
            f'https://{application_vanity_domain}/api/v1/existing-user-invitation/invite-user',
            headers={
                'content-type': 'application/json',
                'accept': 'application/json',
                'authorization': f'Bearer {token}',
            },
            json={'userId': user_id}
        )

    @patch('requests.post')
    def test_invite_existing_user_invalid_tenant(self, mock_post):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "ApplicationId is not valid"}
        mock_post.return_value = mock_response

        token = "valid_token"
        application_vanity_domain = "valid-domain"
        tenant_id = "invalid_tenant"
        identity_provider_name = "idpName"
        user_id = "userXYZ"

        # Act & Assert
        with self.assertRaises(BadRequestError):
            invite_existing_user(
                token=token,
                application_vanity_domain=application_vanity_domain,
                tenant_id=tenant_id,
                identity_provider_name=identity_provider_name,
                user_id=user_id
            )

    @patch('requests.post')
    def test_invite_existing_user_unauthorized(self, mock_post):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.json.return_value = {"error": "Unauthorized"}
        mock_post.return_value = mock_response

        token = "invalid_token"
        application_vanity_domain = "valid-domain"
        tenant_id = "tenant123"
        identity_provider_name = "idpName"
        user_id = "userXYZ"

        # Act & Assert
        with self.assertRaises(AuthorizationError):
            invite_existing_user(
                token=token,
                application_vanity_domain=application_vanity_domain,
                tenant_id=tenant_id,
                identity_provider_name=identity_provider_name,
                user_id=user_id
            )

    def test_invite_existing_user_missing_args(self):
        # Missing token should raise BadRequestError
        with self.assertRaises(BadRequestError):
            invite_existing_user(
                token=None,
                application_vanity_domain="valid-domain",
                tenant_id="tenant123",
                identity_provider_name="idpName",
                user_id="userXYZ"
            )


if __name__ == '__main__':
    unittest.main()