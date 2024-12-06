import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from wristband.users.users_utils import UsersService
from wristband.users.users_service_upload_users_csv import main

class TestUploadUsersCSV(unittest.TestCase):
    @patch.object(UsersService, 'upload_users_csv')
    def test_upload_users_csv_main(self, mock_upload):
        # Arrange
        sys.argv = [
            'users_service_upload_users_csv.py',
            '--token', 'test_token',
            '--application_vanity_domain', 'test-domain',
            '--tenant_id', 'tenant123',
            '--identity_provider_name', 'idpName'
        ]

        # Mock a return value to verify it prints correctly
        mock_upload.return_value = [{'email': 'test@example.com', 'status_code': 201, 'message': 'User invited successfully'}]

        # Use patch to capture printed output if needed
        with patch('sys.stdout', new_callable=lambda: MagicMock()) as mock_stdout:
            # Act
            main()
            
            # Optional: Check if output was printed (if you print results in main)
            # You can do something like:
            # print_calls = [call[0][0] for call in mock_stdout.write.call_args_list]
            # self.assertIn('test@example.com', ''.join(print_calls))

        # Assert
        mock_upload.assert_called_once_with(invite_users=True)

if __name__ == '__main__':
    unittest.main()