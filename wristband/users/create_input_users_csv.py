from wristband.users.users_utils import UsersService

def main():
    # Initialize service without credentials
    service = UsersService()
    service.create_input_users_csv()

if __name__ == "__main__":
    main()