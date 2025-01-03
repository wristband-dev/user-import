import requests
from wristband.exceptions import BadRequestError, AuthorizationError
from wristband.users.models.user import User
import argparse
import json
from dotenv import load_dotenv
import os
from typing import Optional

def create_user(
    user: User,
    token: Optional[str] = None,
    application_vanity_domain: Optional[str] = None,
    tenant_id: Optional[str] = None,
    identity_provider_name: Optional[str] = None
):
    """
    API Docs - https://docs.wristband.dev/reference/createuserv1
    """
    load_dotenv()

    if not token:
        os_token = os.getenv("TOKEN")
        if os_token:
            token = os_token
    if not application_vanity_domain:
        os_application_vanity_domain = os.getenv("APPLICATION_VANITY_DOMAIN")
        if os_application_vanity_domain:
            application_vanity_domain = os_application_vanity_domain
    if not tenant_id:
        os_tenant_id = os.getenv("TENANT_ID")
        if os_tenant_id:
            tenant_id = os_tenant_id
    if not identity_provider_name:
        os_identity_provider_name = os.getenv("IDENTITY_PROVIDER_NAME")
        if os_identity_provider_name:
            identity_provider_name = os_identity_provider_name

    if not token or not application_vanity_domain or not tenant_id or not identity_provider_name:
        raise BadRequestError("Service is not properly initialized with required credentials.")

    # Construct the URL
    url = f'https://{application_vanity_domain}/api/v1/users'

    # Headers to indicate the type of data being sent
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
        'authorization': f'Bearer {token}',
    }

    request_body = {
        'tenantId': tenant_id,
        'identityProviderName': identity_provider_name,
    }

    # Add user fields to the request body
    request_body.update(user.to_dict())

    # Perform the GET request
    response = requests.post(url, headers=headers, json=request_body)

    if response.status_code == 404:
        raise BadRequestError("ApplicationId is not valid - please rerun script & enter a valid applicationId")
    elif response.status_code == 403:
        raise AuthorizationError("Client is not authorized to perform the user import - please make sure that the client has the appropriate permissions assigned to it and then rerun script")

    # Return response
    return response


def main():
    parser = argparse.ArgumentParser(description="Create a new user in the Wristband system.")
    
    parser.add_argument('--token', required=True, help="Authorization token for the API.")
    parser.add_argument('--application_vanity_domain', required=True, help="The vanity domain of the application.")
    parser.add_argument('--tenant_id', required=True, help="Tenant ID for the user creation.")
    parser.add_argument('--identity_provider_name', required=True, help="Identity provider name.")
    parser.add_argument('--user_data', required=True, help="JSON string containing user data.")
    
    args = parser.parse_args()

    # Load user data from JSON string
    try:
        user_dict = json.loads(args.user_data)
        user = User(**user_dict)
    except json.JSONDecodeError as e:
        raise BadRequestError(f"Failed to parse user data JSON: {e}")
    except Exception as e:
        raise BadRequestError(f"Error initializing User object: {e}")

    # Call the create_user function
    response = create_user(
        user=user,
        token=args.token,
        application_vanity_domain=args.application_vanity_domain,
        tenant_id=args.tenant_id,
        identity_provider_name=args.identity_provider_name
    )

    print(f"Response: {response.status_code}")
    print(f"Response Data: {response.json()}")


if __name__ == "__main__":
    main()