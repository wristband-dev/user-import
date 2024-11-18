import argparse
import sys
from wristband.users.users_utils import UsersService
from wristband.exceptions import (
    get_non_empty_response,
    AuthenticationError,
    AuthorizationError,
    BadRequestError,
)

def main():
    parser = argparse.ArgumentParser(description="Upload users from CSV")
    parser.add_argument('--token', type=str, help='Authentication token')
    parser.add_argument('--application_vanity_domain', type=str, help='Application vanity domain')
    parser.add_argument('--tenant_id', type=str, help='Tenant ID')
    parser.add_argument('--identity_provider_name', type=str, help='Identity provider name')
    parser.add_argument('--invite_users', action='store_true', help='Invite users after creation')

    # Parse arguments
    args = parser.parse_args()

    # Ensure required arguments are provided
    required_args = ['token', 'application_vanity_domain', 'tenant_id', 'identity_provider_name']
    missing_args = [arg for arg in required_args if getattr(args, arg) is None]
    if missing_args:
        print(f"Missing required arguments: {', '.join(missing_args)}")
        parser.print_help()
        sys.exit(1)

    # Initialize the service
    service = UsersService(
        token=args.token,
        application_vanity_domain=args.application_vanity_domain,
        tenant_id=args.tenant_id,
        identity_provider_name=args.identity_provider_name
    )

    # Execute the upload_user_csv method
    try:
        logs = service.upload_users_csv(invite_users=args.invite_users)
        for log in logs:
            print(log)
    except (AuthenticationError, AuthorizationError, BadRequestError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()