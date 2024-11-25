from wristband.exceptions import AuthorizationError, BadRequestError
import requests
import argparse
from typing import List
from wristband.roles.models.role import Role
from wristband.roles.models.role_list import RoleList

def assign_roles_to_user(
    token:str,
    application_vanity_domain:str,
    user_id:str,
    roles:List[Role],
):
    """
    API Docs - https://docs.wristband.dev/reference/assignrolestouserv1
    """
    roles = RoleList(roles)

    # Base URL
    url = f'https://{application_vanity_domain}/api/v1/users/{user_id}/assign-roles'

    # Headers to indicate the type of data being sent
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {token}',
        'content-type': 'application/json',
    }

    # Add roles to the payload
    payload = {
        'roleIds': roles.get_role_ids()
    }

    # Perform the POST request
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise BadRequestError(response.json())
    
    return response


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Fetch tenant roles using Wristband API.")
    parser.add_argument("--token", required=True, help="API token for authentication.")
    parser.add_argument("--application_vanity_domain", required=True, help="Application vanity domain.")
    parser.add_argument("--user_id", required=True, help="User ID")
    parser.add_argument("--roles", required=True, help="roles")


    # Parse the arguments
    args = parser.parse_args()

    # Call the function with arguments
    try:
        roles = assign_roles_to_user(
            token=args.token,
            application_vanity_domain=args.application_vanity_domain,
            user_id=args.user_id,
            roles=args.roles
        )
        
    except (AuthorizationError, BadRequestError) as e:
        print(f"Error: {e}")