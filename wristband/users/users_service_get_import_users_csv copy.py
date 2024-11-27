import argparse
from wristband.users.users_utils import UsersService

def main():
    parser = argparse.ArgumentParser(description='Create and import users from CSV.')
    svc = UsersService()
    svc.get_import_users_from_csv()
       

if __name__ == '__main__':
    main()