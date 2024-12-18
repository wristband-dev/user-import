import argparse
from wristband.users.users_utils import UsersService
from typing import Optional
from dotenv import load_dotenv
import os
from wristband.exceptions import BadRequestError

def upload_users_csv(
    token: Optional[str] = None, 
    application_vanity_domain: Optional[str] = None, 
    tenant_id: Optional[str] = None, 
    identity_provider_name: Optional[str] = None, 
):
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

    svc = UsersService(
        token=token,
        application_vanity_domain=application_vanity_domain,
        tenant_id=tenant_id,
        identity_provider_name=identity_provider_name,
    )

    return svc.upload_users_csv(invite_users=True)


def main():
    parser = argparse.ArgumentParser(description="Create a new user in the Wristband system.")
    
    parser.add_argument('--token', required=False, help="Authorization token for the API.")
    parser.add_argument('--application_vanity_domain', required=False, help="The vanity domain of the application.")
    parser.add_argument('--tenant_id', required=False, help="Tenant ID for the user creation.")
    parser.add_argument('--identity_provider_name', required=False, help="Identity provider name.")
    
    args = parser.parse_args()

    print(
        upload_users_csv(
            token=args.token,
            application_vanity_domain=args.application_vanity_domain,
            tenant_id=args.tenant_id,
            identity_provider_name=args.identity_provider_name,
        )
    )

if __name__ == "__main__":
    main()