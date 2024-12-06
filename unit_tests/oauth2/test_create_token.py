import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add two parent directories to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from wristband.oauth2.create_token import create_token

class TestCreateToken(unittest.TestCase):
    @patch('requests.post')
    def test_create_token_success(self, mock_post):
        # Arrange
        # Set up a mock response object with the desired JSON payload
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'access_token': 'test_access_token'}
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Act
        token = create_token(
            application_vanity_domain='valid-domain',
            client_id='valid_client_id',
            client_secret='valid_client_secret'
        )

        # Assert
        self.assertEqual(token, 'test_access_token')
        mock_post.assert_called_once_with(
            'https://valid-domain/api/v1/oauth2/token',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={'grant_type': 'client_credentials'},
            auth=unittest.mock.ANY  # We don't need to assert exact auth object
        )

if __name__ == '__main__':
    unittest.main()