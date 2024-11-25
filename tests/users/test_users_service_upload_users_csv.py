from wristband.users.users_utils import UsersService
from wristband.oauth2.create_token import create_token
import os

application_vanity_domain = os.environ['APPLICATION_VANITY_DOMAIN']
client_id = os.environ['CLIENT_ID'] 
client_secret = os.environ['CLIENT_SECRET']
tenant_id = os.environ['TENANT_ID']
identity_provider_name = os.environ['IDENTITY_PROVIDER_NAME']

token = create_token(
    application_vanity_domain=application_vanity_domain,
    client_id=client_id,
    client_secret=client_secret
)

svc = UsersService(
    token=token,
    application_vanity_domain=application_vanity_domain,
    tenant_id=tenant_id,
    identity_provider_name=identity_provider_name,
)

logs = svc.upload_users_csv(invite_users=True)
