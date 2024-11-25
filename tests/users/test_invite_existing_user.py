from wristband.oauth2.create_token import create_token
from wristband.users.create_user import create_user
from wristband.users.invite_existing_user import invite_existing_user
from wristband.users.models.user import User
import os
import json

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

try: 
    user_id = user_response.json()['id']

    response = invite_existing_user(
        token=token,
        application_vanity_domain=application_vanity_domain,
        tenant_id=tenant_id,
        identity_provider_name=identity_provider_name,
        user_id=user_id
    )
    print(response)
    
    print(f"""
        Check via command args:
            python3 wristband/users/invite_existing_user.py \\
                --token {token} \\
                --application_vanity_domain {application_vanity_domain} \\
                --tenant_id {tenant_id} \\
                --identity_provider_name {identity_provider_name} \\
                --user_id '{user_id}'
        """)


except Exception as e:
    print(e)

