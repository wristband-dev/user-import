import requests
from requests.auth import HTTPBasicAuth

from ..exceptions import (
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