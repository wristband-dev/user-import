# wristband-python


## Setup Instructions

1. **Create a Virtual Environment**

   To keep your project's dependencies isolated, it's recommended to use a virtual environment. You can create one using the following command:
   ```bash
   python3 -m venv .venv
   ```

2.  **Activate the Virtual Environment**

    Activate the virtual environment to ensure that any packages you install are confined to this environment.
    - On Windows:
    ```bash
    .venv\Scripts\activate
    ```

    - On macOS/Linux:
    ```bash
    source .venv/bin/activate
    ```

3.	**Install the Dependencies**

    With the virtual environment activated, install all required Python packages using:
    ```bash
    pip install -r requirements.txt
    ```


4.  **Configure Environment Variables**

    Copy the example environment file and fill in your specific details:
    ```bash
    cp .env.example .env
    ```
    Open the .env file in a text editor and replace the placeholder values with your actual Wristband credentials

    Example .env file:
    ```ini
    APPLICATION_VANITY_DOMAIN=you_application_vanity_domain
    CLIENT_ID=your_client_id
    CLIENT_SECRET=your_client_secret
    TENANT_ID=your_tenant_id
    IDENTITY_PROVIDER_ID="wristband"
    ```


## Import Users Instructions

1. **Generate Import Users CSV**
    #### Python
    ```python 
    svc = UsersService()
    svc.create_import_users_csv()
    ```
    #### Command Args
    ```bash
    python3 wristband/users/users_service_create_import_users_csv.py 
    ```

2. **Enter user information to csv**

    Enter the "Role Name" field
    - ex: "app:invoexp:owner"
    - if you want to add multiple roles to a user, seperate by commas

3. **Create a Token**
    #### Python
    ```python 
    from wristband.oauth2.create_token import create_token
    token = create_token(
        application_vanity_domain, # Optional if using .env
        client_id, # Optional if using .env
        client_secret, # Optional if using .env
    )
    ```
    #### Command Args
    **Note:** Argumenets are optional if using .env
    ```bash
    python3 wristband/oauth2/create_token.py \
        --application_vanity_domain {application_vanity_domain} \
        --client_id {client_id} \
        --client_secret {client_secret}
    ```

4. **Upload Users CSV to Wristband**
    #### Python
    ```python 
    from wristband.users.upload_users_csv import upload_users_csv
    upload_users_csv(
        token, # Optional if using .env
        application_vanity_domain, # Optional if using .env
        tenant_id, # Optional if using .env
        identity_provider_name, # Optional if using .env
    )
    ```
    #### Command Args
    **Note:** Argumenets are optional if using .env
    ```bash
    python3 wristband/users/users_service_upload_users_csv.py \\
        --token {token} \\
        --application_vanity_domain {application_vanity_domain} \\
        --tenant_id {tenant_id} \\
        --identity_provider_name {identity_provider_name}
    ```