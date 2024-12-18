import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add two parent directories to Python path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from wristband.users.users_utils import UsersService
from wristband.users.create_import_users_csv import main

class TestCreateImportUsersCSV(unittest.TestCase):
    @patch.object(UsersService, 'create_import_users_csv')
    def test_create_import_users_csv_main(self, mock_create):
        sys.argv = ['users_service_create_import_users_csv.py']

        # Act
        main()

        # Assert
        mock_create.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()