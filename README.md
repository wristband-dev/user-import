<div align="center">
  <a href="https://wristband.dev">
    <picture>
      <img src="https://assets.wristband.dev/images/email_branding_logo_v1.png" alt="Github" width="297" height="64">
    </picture>
  </a>
  <p align="center">
    Enterprise-ready auth that is secure by default, truly multi-tenant, and ungated for small businesses.
  </p>
  <p align="center">
    <b>
      <a href="https://wristband.dev">Website</a> •
      <a href="https://docs.wristband.dev/docs/getting-started">Documentation</a>
    </b>
  </p>
</div>

<br/>

---

<br/>

# Wristband User Import Script

A Python script that processes a CSV file containing user information and creates users within a specified tenant of your Wristband application.


## Setup Instructions

1. **Clone Repo**
    ```bash
   git clone https://github.com/wristband-dev/user-import.git
   ```

2. **Open terminal or IDE at project route**

3. **Create a Virtual Environment**

   To keep your project's dependencies isolated, it's recommended to use a virtual environment. You can create one using the following command:
   ```bash
   python3 -m venv .venv
   ```

4.  **Activate the Virtual Environment**

    Activate the virtual environment to ensure that any packages you install are confined to this environment.
    - On Windows:
    ```bash
    .venv\Scripts\activate
    ```

    - On macOS/Linux:
    ```bash
    source .venv/bin/activate
    ```

5.	**Install the Dependencies**

    With the virtual environment activated, install all required Python packages using:
    ```bash
    pip install -r requirements.txt
    ```

6.	**Build the distribution locally**

    ```bash
    pip install -e .
    ```


7.  **Configure Environment Variables**

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
    IDENTITY_PROVIDER_NAME="wristband"
    ```


## Import Users Instructions

1. **Generate Import Users CSV**
    #### Python
    ```python 
    from wristband.users.users_utils import UsersService
    svc = UsersService()
    svc.create_import_users_csv()
    ```
    #### Command Args
    ```bash
    python3 wristband/users/create_import_users_csv.py 
    ```

2. **Enter user information to csv**

    Enter the "Role Name" field
    - ex: "app:invoexp:owner"
    - if you want to add multiple roles to a user, seperate by commas

3. **Upload Users CSV to Wristband**
    #### Python
    ```python 
    from wristband.users.upload_users_csv import upload_users_csv
    upload_users_csv(
        invite_users: bool = False
        application_vanity_domain: Optional[str] = None, # Optional if using .env
        client_id: Optional[str] = None, # Optional if using .env
        client_secret: Optional[str] = None, # Optional if using .env
        tenant_id: Optional[str] = None, # Optional if using .env
        identity_provider_name: Optional[str] = None, # Optional if using .env
    )
    ```
    #### Command Args
    **Note:** Argumenets are optional if using .env
    ```bash
    python3 wristband/users/upload_users_csv.py \
        --invite_users {invite_users} \
        --application_vanity_domain {application_vanity_domain} \
        --client_id {client_id} \
        --client_secret {client_secret} \
        --tenant_id {tenant_id} \
        --identity_provider_name {identity_provider_name}
    ```
