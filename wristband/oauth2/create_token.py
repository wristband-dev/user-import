import requests
from requests.auth import HTTPBasicAuth
from wristband.exceptions import (
    AuthenticationError,
    AuthorizationError,
    BadRequestError,
)
import argparse


def create_token(
        application_vanity_domain:str, 
        client_id:str, 
        client_secret:str
):
    """
    API Docs - https://docs.wristband.dev/reference/tokenv1
    """

    if not application_vanity_domain or not client_id or not client_secret:
        raise BadRequestError(
            "Service is not properly initialized with required credentials."
        )

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
        response = requests.post(
            url,
            headers=headers,
            data=payload,
            auth=HTTPBasicAuth(client_id, client_secret)
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            raise AuthenticationError(
                "Client credentials are not valid - please rerun script & enter valid credentials"
            ) from http_err
        elif response.status_code == 400:
            raise BadRequestError(
                "Application vanity domain is not valid - please rerun script & enter valid credentials"
            ) from http_err
        else:
            raise AuthorizationError(
                f"HTTP error occurred: {http_err}"
            ) from http_err
    except requests.exceptions.RequestException as err:
        raise BadRequestError(
            "Domain name is not valid - please rerun script & enter a valid domain name"
        ) from err

    # Return the access token from the response JSON
    return response.json().get('access_token')


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate an access token using client credentials.")
    parser.add_argument('--application_vanity_domain', required=True, help="The vanity domain of the application.")
    parser.add_argument('--client_id', required=True, help="The client ID for authentication.")
    parser.add_argument('--client_secret', required=True, help="The client secret for authentication.")
    
    # Parse command-line arguments
    args = parser.parse_args()

    try:
        # Call the create_token function
        token = create_token(
            application_vanity_domain=args.application_vanity_domain,
            client_id=args.client_id,
            client_secret=args.client_secret
        )
        print(f"Access Token: {token}")
    except (AuthenticationError, AuthorizationError, BadRequestError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()