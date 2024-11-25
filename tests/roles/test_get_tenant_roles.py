from wristband.oauth2.create_token import create_token
from wristband.roles.get_tenant_roles import get_tenant_roles
import os

application_vanity_domain = os.environ['APPLICATION_VANITY_DOMAIN']
client_id = os.environ['CLIENT_ID'] 
client_secret = os.environ['CLIENT_SECRET']
tenant_id = os.environ['TENANT_ID']

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

print(tenant_roles)
print(f"""
Check via command args:
    python3 wristband/roles/get_tenant_roles.py \\
        --token {token} \\
        --application_vanity_domain {application_vanity_domain} \\
        --tenant_id {tenant_id}
""")
