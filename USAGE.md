# Wristband Python Usage

## Create a Token
### Python
```python 
from wristband.oauth2.create_token import create_token
token = create_token(
    application_vanity_domain=application_vanity_domain,
    client_id=client_id,
    client_secret=client_secret,
)
```
### Command Args
```bash
python3 wristband/oauth2/create_token.py \\
    --application_vanity_domain {application_vanity_domain} \\
    --client_id {client_id} \\
    --client_secret {client_secret}
```

## Create User
### Python
```python 
from wristband.oauth2.create_token import create_token
from wristband.users.create_user import create_user
from wristband.users.models.user import User
user = User(
    email="frankdonatodiferd@gmail.com",
    givenName="Test",
)
response = create_user(
    token=token,
    application_vanity_domain=application_vanity_domain,
    tenant_id=tenant_id,
    identity_provider_name=identity_provider_name,
    user=user
)
```
### Command Args
```json
user_dict = {
    "email": "frankdonatodiferd@gmail.com",
    "givenName": "Test",
    "displayName": "Test User",
}
```
```bash
python3 wristband/users/create_user.py \\
    --token {token} \\
    --application_vanity_domain {application_vanity_domain} \\
    --tenant_id {tenant_id} \\
    --identity_provider_name {identity_provider_name} \\
    --user_data user_dict
```

## Invite Existing User
### Python
```python 
from wristband.oauth2.create_token import create_token
from wristband.users.create_user import create_user
from wristband.users.invite_existing_user import invite_existing_user
from wristband.users.models.user import User
user_id = user_response.json()['id']
response = invite_existing_user(
    token=token,
    application_vanity_domain=application_vanity_domain,
    tenant_id=tenant_id,
    identity_provider_name=identity_provider_name,
    user_id=user_id
)
```
### Command Args
```bash
python3 wristband/users/invite_existing_user.py \\
    --token {token} \\
    --application_vanity_domain {application_vanity_domain} \\
    --tenant_id {tenant_id} \\
    --identity_provider_name {identity_provider_name} \\
    --user_id '{user_id}'
```

## Users Service
1. Create Import Users CSV
### Python
```python 
svc = UsersService()
svc.create_import_users_csv()
```
### Command Args
```bash
python3 wristband/users/users_service_create_import_users_csv.py 
```
2. Get Import Users CSV
### Python
```python 
from wristband.users.users_utils import UsersService
svc = UsersService()
svc.create_import_users_csv()
```
### Command Args
```bash
python3 wristband/users/users_service_get_import_users_csv.py 
```
3. Upload Users CSV
### Python
```python 
from wristband.users.users_utils import UsersService
svc = UsersService(
    token=token,
    application_vanity_domain=application_vanity_domain,
    tenant_id=tenant_id,
    identity_provider_name=identity_provider_name,
)

logs = svc.upload_users_csv(invite_users=True)
```
### Command Args
```bash
python3 wristband/oauth2/users_service_upload_users_csv.py \\
    --token {token} \\
    --application_vanity_domain {application_vanity_domain} \\
    --tenant_id {tenant_id} \\
    --identity_provider_name {identity_provider_name}
```

## Get Tenant Roles
### Python
```python 
from wristband.roles.get_tenant_roles import get_tenant_roles
tenant_roles = get_tenant_roles(
    token=token,
    application_vanity_domain=application_vanity_domain,
    tenant_id=tenant_id
)
```
### Command Args
```bash
python3 wristband/roles/get_tenant_roles.py \\
    --token {token} \\
    --application_vanity_domain {application_vanity_domain} \\
    --tenant_id {tenant_id}
```

## Assign Roles to User
### Python
```python 
from wristband.roles.assign_roles_to_user import assign_roles_to_user
assign_roles_to_user(
        token=token,
        application_vanity_domain=application_vanity_domain,
        user_id=user_id,
        roles=filtered_roles
    )
```
### Command Args
```bash
python3 wristband/oauth2/assign_roles_to_user.py \\
    --token {token} \\
    --application_vanity_domain {application_vanity_domain} \\
    --tenant_id {tenant_id} \\
    --roles {roles}
```