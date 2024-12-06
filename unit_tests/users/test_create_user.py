import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add two parent directories to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from wristband.exceptions import BadRequestError, AuthorizationError
from wristband.users.models.user import User
from wristband.users.create_user import create_user

class TestCreateUser(unittest.TestCase):
    @patch('requests.post')
    def test_create_user_success(self, mock_post):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": "new_user_id",
            "tenantId": "tenant123",
            "identityProviderName": "idpName"
        }
        mock_post.return_value = mock_response

        token = "valid_token"
        application_vanity_domain = "valid-domain"
        tenant_id = "tenant123"
        identity_provider_name = "idpName"
        # Use fields that actually exist in User
        user = User(email="john@example.com", fullName="John Doe")

        # Act
        response = create_user(
            token=token,
            application_vanity_domain=application_vanity_domain,
            tenant_id=tenant_id,
            identity_provider_name=identity_provider_name,
            user=user
        )

        # Assert
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"id": "new_user_id", "tenantId": "tenant123", "identityProviderName": "idpName"})
        mock_post.assert_called_once_with(
            f'https://{application_vanity_domain}/api/v1/users',
            headers={
                'content-type': 'application/json',
                'accept': 'application/json',
                'authorization': f'Bearer {token}',
            },
            json={
                'tenantId': tenant_id,
                'identityProviderName': identity_provider_name,
                # user.to_dict() will include 'email' and 'fullName'
                **user.to_dict()
            }
        )

    @patch('requests.post')
    def test_create_user_invalid_tenant(self, mock_post):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "ApplicationId is not valid"}
        mock_post.return_value = mock_response

        token = "valid_token"
        application_vanity_domain = "valid-domain"
        tenant_id = "invalid_tenant"
        identity_provider_name = "idpName"
        user = User(email="john@example.com", fullName="John Doe")

        # Act & Assert
        with self.assertRaises(BadRequestError):
            create_user(
                token=token,
                application_vanity_domain=application_vanity_domain,
                tenant_id=tenant_id,
                identity_provider_name=identity_provider_name,
                user=user
            )

    @patch('requests.post')
    def test_create_user_unauthorized(self, mock_post):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.json.return_value = {"error": "Unauthorized"}
        mock_post.return_value = mock_response

        token = "invalid_token"
        application_vanity_domain = "valid-domain"
        tenant_id = "tenant123"
        identity_provider_name = "idpName"
        user = User(email="john@example.com", fullName="John Doe")

        # Act & Assert
        with self.assertRaises(AuthorizationError):
            create_user(
                token=token,
                application_vanity_domain=application_vanity_domain,
                tenant_id=tenant_id,
                identity_provider_name=identity_provider_name,
                user=user
            )

    def test_create_user_missing_args(self):
        # Missing token should raise BadRequestError
        user = User(email="jane@example.com", fullName="Jane Doe")
        with self.assertRaises(BadRequestError):
            create_user(
                token=None,
                application_vanity_domain="valid-domain",
                tenant_id="tenant123",
                identity_provider_name="idpName",
                user=user
            )


if __name__ == '__main__':
    unittest.main()