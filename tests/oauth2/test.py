import unittest
from unittest.mock import patch, Mock
import sys
import json
import requests

# Assuming the code above is saved in a file named 'token_module.py'
from token_module import create_token, main
from wristband.exceptions import (
    AuthenticationError,
    AuthorizationError,
    BadRequestError,
)

class TestCreateToken(unittest.TestCase):

    @patch('token_module.requests.post')
    def test_create_token_success(self, mock_post):
        """Test create_token function with valid inputs."""
        # Mock the response of requests.post to simulate a successful token generation
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'access_token': 'fake_token'}
        mock_post.return_value = mock_response

        application_vanity_domain = 'example.com'
        client_id = 'valid_client_id'
        client_secret = 'valid_client_secret'

        token = create_token(application_vanity_domain, client_id, client_secret)
        self.assertEqual(token, 'fake_token')

        # Ensure requests.post was called with the expected arguments
        expected_url = f'https://{application_vanity_domain}/api/v1/oauth2/token'
        expected_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        expected_data = {'grant_type': 'client_credentials'}
        expected_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)

        mock_post.assert_called_with(
            expected_url,
            headers=expected_headers,
            data=expected_data,
            auth=expected_auth
        )

    @patch('token_module.requests.post')
    def test_create_token_authentication_error(self, mock_post):
        """Test create_token function with invalid credentials leading to AuthenticationError."""
        # Simulate a 401 Unauthorized response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_post.return_value = mock_response

        application_vanity_domain = 'example.com'
        client_id = 'invalid_client_id'
        client_secret = 'invalid_client_secret'

        with self.assertRaises(AuthenticationError):
            create_token(application_vanity_domain, client_id, client_secret)

    @patch('token_module.requests.post')
    def test_create_token_bad_request_error(self, mock_post):
        """Test create_token function with invalid domain leading to BadRequestError."""
        # Simulate a 400 Bad Request response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_post.return_value = mock_response

        application_vanity_domain = 'invalid_domain'
        client_id = 'client_id'
        client_secret = 'client_secret'

        with self.assertRaises(BadRequestError):
            create_token(application_vanity_domain, client_id, client_secret)

    @patch('token_module.requests.post')
    def test_create_token_authorization_error(self, mock_post):
        """Test create_token function with unexpected HTTP error leading to AuthorizationError."""
        # Simulate a 403 Forbidden response
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_post.return_value = mock_response

        application_vanity_domain = 'example.com'
        client_id = 'client_id'
        client_secret = 'client_secret'

        with self.assertRaises(AuthorizationError):
            create_token(application_vanity_domain, client_id, client_secret)

    def test_create_token_missing_arguments(self):
        """Test create_token function with missing arguments leading to BadRequestError."""
        with self.assertRaises(BadRequestError):
            create_token(None, 'client_id', 'client_secret')
        with self.assertRaises(BadRequestError):
            create_token('domain', None, 'client_secret')
        with self.assertRaises(BadRequestError):
            create_token('domain', 'client_id', None)

    @patch('token_module.requests.post')
    def test_command_line_success(self, mock_post):
        """Test main function with valid command-line arguments."""
        # Mock the response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'access_token': 'fake_token'}
        mock_post.return_value = mock_response

        testargs = [
            'script_name',
            '--application_vanity_domain', 'example.com',
            '--client_id', 'valid_client_id',
            '--client_secret', 'valid_client_secret'
        ]
        with patch.object(sys, 'argv', testargs):
            with patch('builtins.print') as mock_print:
                main()
                mock_print.assert_called_with('Access Token: fake_token')

    @patch('token_module.requests.post')
    def test_command_line_missing_arguments(self, mock_post):
        """Test main function with missing command-line arguments."""
        testargs = [
            'script_name',
            '--application_vanity_domain', 'example.com',
            '--client_id', 'valid_client_id'
        ]
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit):
                main()

    @patch('token_module.requests.post')
    def test_command_line_authentication_error(self, mock_post):
        """Test main function with invalid credentials leading to AuthenticationError."""
        # Simulate a 401 Unauthorized response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_post.return_value = mock_response

        testargs = [
            'script_name',
            '--application_vanity_domain', 'example.com',
            '--client_id', 'invalid_client_id',
            '--client_secret', 'invalid_client_secret'
        ]
        with patch.object(sys, 'argv', testargs):
            with patch('builtins.print') as mock_print:
                main()
                mock_print.assert_called_with(
                    'Error: Client credentials are not valid - please rerun script & enter valid credentials'
                )

if __name__ == '__main__':
    unittest.main()