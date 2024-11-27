import argparse
from wristband.users.users_utils import UsersService

def main():
    parser = argparse.ArgumentParser(description="Create a new user in the Wristband system.")
    
    parser.add_argument('--token', required=True, help="Authorization token for the API.")
    parser.add_argument('--application_vanity_domain', required=True, help="The vanity domain of the application.")
    parser.add_argument('--tenant_id', required=True, help="Tenant ID for the user creation.")
    parser.add_argument('--identity_provider_name', required=True, help="Identity provider name.")
    
    args = parser.parse_args()

    svc = UsersService(
        token=args.token,
        application_vanity_domain=args.application_vanity_domain,
        tenant_id=args.tenant_id,
        identity_provider_name=args.identity_provider_name,
    )

    print(svc.upload_users_csv(invite_users=True))


if __name__ == "__main__":
    main()