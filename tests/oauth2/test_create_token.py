from wristband.oauth2.create_token import create_token
import os

application_vanity_domain = os.environ['APPLICATION_VANITY_DOMAIN']
client_id = os.environ['CLIENT_ID'] 
client_secret = os.environ['CLIENT_SECRET']

token = create_token(
    application_vanity_domain=application_vanity_domain,
    client_id=client_id,
    client_secret=client_secret,
)

print(f"Access Token: {token}")
print(f"""
Check via command args:
    python3 wristband/oauth2/create_token.py \\
        --application_vanity_domain {application_vanity_domain} \\
        --client_id {client_id} \\
        --client_secret {client_secret}
""")