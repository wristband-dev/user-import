import argparse
from wristband.users.users_utils import UsersService
from typing import Optional
from dotenv import load_dotenv
import os
from wristband.exceptions import BadRequestError
from wristband.oauth2.create_token import create_token

def upload_users_csv(
    invite_users: bool = False,
    application_vanity_domain: Optional[str] = None, 
    client_id: Optional[str] = None, 
    client_secret: Optional[str] = None,
    tenant_id: Optional[str] = None, 
    identity_provider_name: Optional[str] = None, 
):
    load_dotenv()
    
    if not application_vanity_domain:
        os_application_vanity_domain = os.getenv("APPLICATION_VANITY_DOMAIN")
        if os_application_vanity_domain:
            application_vanity_domain = os_application_vanity_domain
    if not client_id:
        os_client_id = os.getenv("CLIENT_ID")
        if os_client_id:
            client_id = os_client_id
    if not client_secret:
        os_client_secret = os.getenv("CLIENT_SECRET")
        if os_client_secret:
            client_secret = os_client_secret
    if not tenant_id:
        os_tenant_id = os.getenv("TENANT_ID")
        if os_tenant_id:
            tenant_id = os_tenant_id
    if not identity_provider_name:
        os_identity_provider_name = os.getenv("IDENTITY_PROVIDER_NAME")
        if os_identity_provider_name:
            identity_provider_name = os_identity_provider_name

    if not application_vanity_domain or not client_id or not client_secret or not tenant_id or not identity_provider_name:
        raise BadRequestError("Service is not properly initialized with required credentials.")
    
    token = create_token(
        application_vanity_domain=application_vanity_domain,
        client_id=client_id,
        client_secret=client_secret,
    )

    if not token:
        raise BadRequestError("Token not generated.")

    svc = UsersService(
        token=token,
        application_vanity_domain=application_vanity_domain,
        tenant_id=tenant_id,
        identity_provider_name=identity_provider_name,
    )

    return svc.upload_users_csv(invite_users=invite_users)


def main():
    parser = argparse.ArgumentParser(description="Create a new user in the Wristband system.")
    
    parser.add_argument('--invite_users', required=False, help="Flag to invite users.", default=False)
    parser.add_argument('--application_vanity_domain', required=False, help="The vanity domain of the application.")
    parser.add_argument('--client_id', required=False, help="Client ID for the API.")
    parser.add_argument('--client_secret', required=False, help="Client secret for the API.")
    parser.add_argument('--tenant_id', required=False, help="Tenant ID for the user creation.")
    parser.add_argument('--identity_provider_name', required=False, help="Identity provider name.")
    
    args = parser.parse_args()

    print(
        upload_users_csv(
            invite_users=args.invite_users,
            application_vanity_domain=args.application_vanity_domain,
            client_id=args.client_id,
            client_secret=args.client_secret,
            tenant_id=args.tenant_id,
            identity_provider_name=args.identity_provider_name,
        )
    )

if __name__ == "__main__":
    main()