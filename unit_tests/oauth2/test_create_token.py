import unittest
from unittest.mock import patch, MagicMock
from wristband.users.models.user import User
from wristband.exceptions import BadRequestError, AuthorizationError
from wristband.oauth2.create_token import create_token


class TestCreateUser(unittest.TestCase):
    def setUp(self):
        self.token = "test_token"
        self.application_vanity_domain = "test.vanity.domain"
        self.tenant_id = "test_tenant"
        self.identity_provider_name = "test_provider"
        self.user = User(id="123", email="test@example.com", name="Test User")

    @patch('requests.post')
    def test_create_user_success(self, mock_post):
        # Mocking the response from requests.post
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_post.return_value = mock_response

        # Call the function
        response = create_token(
            token=self.token,
            application_vanity_domain=self.application_vanity_domain,
            tenant_id=self.tenant_id,
            identity_provider_name=self.identity_provider_name,
            user=self.user
        )

        # Assertions
        mock_post.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True})

    @patch('requests.post')
    def test_create_user_bad_request_error(self, mock_post):
        # Mocking the response for a 404 error
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_post.return_value = mock_response

        with self.assertRaises(BadRequestError):
            create_token(
                token=self.token,
                application_vanity_domain=self.application_vanity_domain,
                tenant_id=self.tenant_id,
                identity_provider_name=self.identity_provider_name,
                user=self.user
            )

    @patch('requests.post')
    def test_create_user_authorization_error(self, mock_post):
        # Mocking the response for a 403 error
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_post.return_value = mock_response

        with self.assertRaises(AuthorizationError):
            create_token(
                token=self.token,
                application_vanity_domain=self.application_vanity_domain,
                tenant_id=self.tenant_id,
                identity_provider_name=self.identity_provider_name,
                user=self.user
            )

    def test_create_user_missing_parameters(self):
        # Test for missing parameters
        with self.assertRaises(BadRequestError):
            create_token(
                token=None,
                application_vanity_domain=self.application_vanity_domain,
                tenant_id=self.tenant_id,
                identity_provider_name=self.identity_provider_name,
                user=self.user
            )


if __name__ == "__main__":
    unittest.main()