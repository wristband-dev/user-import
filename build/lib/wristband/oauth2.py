import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

class AuthenticationError(Exception):
    """Custom exception for authentication failures."""
    pass

class AuthorizationError(Exception):
    """Custom exception for authorization failures."""
    pass

class BadRequestError(Exception):
    """Custom exception for bad request errors."""
    pass


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
    
