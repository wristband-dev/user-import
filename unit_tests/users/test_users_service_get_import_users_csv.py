import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from wristband.users.users_utils import UsersService
from wristband.users.users_service_get_import_users_csv import main

class TestGetImportUsersCSV(unittest.TestCase):
    @patch.object(UsersService, 'get_import_users_from_csv')
    def test_get_import_users_csv_main(self, mock_get_users):
        # Arrange
        sys.argv = ['users_service_get_import_users_csv.py']
        
        # Mock return value
        mock_get_users.return_value = []

        # Act
        main()

        # Assert
        mock_get_users.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()