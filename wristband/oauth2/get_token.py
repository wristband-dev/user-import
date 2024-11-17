import argparse

from .token_utils import get_token
from ..exceptions import (
    get_non_empty_response,
    AuthenticationError,
    AuthorizationError,
    BadRequestError,
)

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Get an OAuth2 access token.")

    # Add arguments
    parser.add_argument('--application_vanity_domain', type=str, help='Application vanity domain')
    parser.add_argument('--client_id', type=str, help='Client ID')
    parser.add_argument('--client_secret', type=str, help='Client Secret')

    # Parse arguments
    args = parser.parse_args()

    # Check if arguments were provided, otherwise prompt the user
    application_vanity_domain = args.application_vanity_domain or \
        get_non_empty_response("Enter the application vanity domain: ")
    client_id = args.client_id or \
        get_non_empty_response("Enter the client ID: ")
    client_secret = args.client_secret or \
        get_non_empty_response("Enter the client secret: ")

    try:
        token = get_token(application_vanity_domain, client_id, client_secret)
        print(f"{token}")
    except (AuthenticationError, AuthorizationError, BadRequestError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()