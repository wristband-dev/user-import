from wristband.users.users_utils import UsersService

svc = UsersService()
users = svc.get_import_users_from_csv()
print(users)