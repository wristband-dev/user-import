from wristband.oauth2.create_token import create_token
from wristband.roles.get_tenant_roles import get_tenant_roles
from wristband.users.create_user import create_user
from wristband.users.models.user import User
from wristband.roles.assign_roles_to_user import assign_roles_to_user
import os

application_vanity_domain = os.environ['APPLICATION_VANITY_DOMAIN']
client_id = os.environ['CLIENT_ID'] 
client_secret = os.environ['CLIENT_SECRET']
tenant_id = os.environ['TENANT_ID']
identity_provider_name = os.environ['IDENTITY_PROVIDER_NAME']

token = create_token(
    application_vanity_domain=application_vanity_domain,
    client_id=client_id,
    client_secret=client_secret,
)

tenant_roles = get_tenant_roles(
    token=token,
    application_vanity_domain=application_vanity_domain,
    tenant_id=tenant_id
)

filtered_roles = [role for role in tenant_roles if role['displayName'] == 'owner']

user = User(
    email="frankdonatodiferd@gmail.com",
    givenName="Test",
)

user_response = create_user(
    token=token,
    application_vanity_domain=application_vanity_domain,
    tenant_id=tenant_id,
    identity_provider_name=identity_provider_name,
    user=user
)

if user_response.status_code == 201:
    user_id = user_response.json().get('id')

    assign_roles_to_user(
        token=token,
        application_vanity_domain=application_vanity_domain,
        user_id=user_id,
        roles=filtered_roles
    )
else:
    print(user_response.json())

