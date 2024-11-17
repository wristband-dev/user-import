import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import argparse
from ..exceptions import (
    get_non_empty_response,
    AuthenticationError,
    AuthorizationError,
    BadRequestError,
)


def get_token(application_vanity_domain, client_id, client_secret):
    # Construct the URL
    url = f'https://{application_vanity_domain}/api/v1/oauth2/token'

    # Headers to indicate the type of data being sent
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    # Data payload
    payload = {
        'grant_type': 'client_credentials',
    }

    try:
        # Make the request using HTTP Basic Authentication
        response = requests.post(url, headers=headers, data=payload, auth=HTTPBasicAuth(client_id, client_secret))

    except:
        raise BadRequestError("Domain name is not valid - please rerun script & enter a valid domain name")

    if response.status_code == 401:
        raise AuthenticationError("Client credentials are not valid - please rerun script & enter valid credentials")
    elif response.status_code == 400:
        raise BadRequestError("Application vanity domain is not valid - please rerun script & enter valid credentials")
    
    # Return json
    return response.json().get('access_token')
    
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
    application_vanity_domain = args.application_vanity_domain or get_non_empty_response("Enter the application vanity domain: ")
    client_id = args.client_id or get_non_empty_response("Enter the client ID: ")
    client_secret = args.client_secret or get_non_empty_response("Enter the client secret: ")

    try:
        token = get_token(application_vanity_domain, client_id, client_secret)
        print(f"{token}")
    except (AuthenticationError, AuthorizationError, BadRequestError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()