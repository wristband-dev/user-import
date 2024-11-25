from wristband.users.models.user import User
from wristband.exceptions import BadRequestError, AuthorizationError
import requests
import argparse

def invite_existing_user(
    token: str,
    application_vanity_domain: str,
    tenant_id: str,
    identity_provider_name: str,
    user_id: str,
):
    """
    API Docs - https://docs.wristband.dev/reference/inviteexistinguserv1
    """
    if not token or not application_vanity_domain or not tenant_id or not identity_provider_name:
        raise BadRequestError("Service is not properly initialized with required credentials.")

    # Construct the URL
    url = f'https://{application_vanity_domain}/api/v1/existing-user-invitation/invite-user'

    # Headers to indicate the type of data being sent
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
        'authorization': f'Bearer {token}',
    }

    # Construct the request body
    request_body = {
        'userId': user_id
    }

    # Perform the POST request with JSON payload
    response = requests.post(url, headers=headers, json=request_body)

    if response.status_code == 404:
        raise BadRequestError("ApplicationId is not valid - please rerun script & enter a valid applicationId")
    elif response.status_code == 403:
        raise AuthorizationError("Client is not authorized to perform the user export - please make sure that the client has the appropriate permissions assigned to it and then rerun script")

    # Return response
    return response          
    


def main():
    parser = argparse.ArgumentParser(description="Invite an existing user using the Wristband API.")

    parser.add_argument('--token', required=True, help="Authorization token for the API.")
    parser.add_argument('--application_vanity_domain', required=True, help="The vanity domain of the application.")
    parser.add_argument('--tenant_id', required=True, help="Tenant ID for the user invitation.")
    parser.add_argument('--identity_provider_name', required=True, help="Identity provider name.")
    parser.add_argument('--user_id', required=True, help="The ID of the user to invite.")

    args = parser.parse_args()

    try:
        # Call the invite_existing_user function
        response = invite_existing_user(
            token=args.token,
            application_vanity_domain=args.application_vanity_domain,
            tenant_id=args.tenant_id,
            identity_provider_name=args.identity_provider_name,
            user_id=args.user_id
        )

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Data: {response.json()}")
    except BadRequestError as e:
        print(f"BadRequestError: {e}")
    except AuthorizationError as e:
        print(f"AuthorizationError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()