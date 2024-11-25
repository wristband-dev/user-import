from wristband.exceptions import AuthorizationError, BadRequestError
import requests
from wristband.roles.models.roles_response import RolesResponse
from wristband.roles.models.role_list import RoleList
import json
import argparse

def get_tenant_roles(
    token:str,
    application_vanity_domain:str,
    tenant_id:str
) -> RoleList:
    """
    API Docs - https://docs.wristband.dev/reference/querytenantrolesv1
    Implements pagination to retrieve all roles.
    """
    if not token or not application_vanity_domain or not tenant_id:
        raise BadRequestError("Service is not properly initialized with required credentials.")

    # Base URL
    base_url = f'https://{application_vanity_domain}/api/v1/tenants/{tenant_id}/roles'

    # Headers to indicate the type of data being sent
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {token}',
        'host': f'{application_vanity_domain}',
        'content-type': 'application/json',
    }

    # Pagination parameters
    start_index = 1
    items_per_page = 20
    all_roles = []

    while True:
        # Construct the URL with pagination
        url = f"{base_url}?include_application_roles=true&fields=id,name,displayName&sort_by=displayName:asc&startIndex={start_index}&count={items_per_page}"

        # Perform the GET request
        response = requests.get(url, headers=headers)

        if response.status_code == 404:
            raise BadRequestError("ApplicationId is not valid - please rerun script & enter a valid applicationId")
        elif response.status_code == 403:
            raise AuthorizationError("Client is not authorized to perform the user export - please make sure that the client has the appropriate permissions assigned to it and then rerun script")

        # Parse the response
        json_data = response.json()

        # Convert to RolesResponse
        roles_response = RolesResponse.from_json(json.dumps(json_data))

        # Add current page roles to the list
        all_roles.extend(roles_response.items)

        # Check if there are more items to fetch
        total_results = roles_response.totalResults
        start_index += items_per_page

        if start_index > total_results:
            break

    return all_roles


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Fetch tenant roles using Wristband API.")
    parser.add_argument("--token", required=True, help="API token for authentication.")
    parser.add_argument("--application_vanity_domain", required=True, help="Application vanity domain.")
    parser.add_argument("--tenant_id", required=True, help="Tenant ID.")

    # Parse the arguments
    args = parser.parse_args()

    # Call the function with arguments
    try:
        roles = get_tenant_roles(
            token=args.token,
            application_vanity_domain=args.application_vanity_domain,
            tenant_id=args.tenant_id
        )
        print(roles)
    except (AuthorizationError, BadRequestError) as e:
        print(f"Error: {e}")