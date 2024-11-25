import pandas as pd
from datetime import datetime
import os
from typing import List
from wristband.users.models.user import User
from wristband.users.create_user import create_user
from wristband.users.invite_existing_user import invite_existing_user
from wristband.roles.get_tenant_roles import get_tenant_roles
from wristband.roles.assign_roles_to_user import assign_roles_to_user


class UsersService:
    def __init__(
        self, 
        token:str = None,
        application_vanity_domain:str = None, 
        tenant_id:str = None, 
        identity_provider_name:str = None
    ):

        self.token = token
        self.application_vanity_domain = application_vanity_domain
        self.tenant_id = tenant_id
        self.identity_provider_name = identity_provider_name

        self.import_file_path = 'import_users.csv'

    def upload_users_csv(
        self,
        invite_users = True
    ): 
        """
        Reads a CSV file and uploads the users to Wristband.
        """
        # Init
        logs = []
        did_fetch_roles = False

        # Get users
        users = self.get_import_users_from_csv()
        for user in users:
            
            response = create_user(
                token=self.token,
                application_vanity_domain=self.application_vanity_domain,
                tenant_id=self.tenant_id,
                identity_provider_name=self.identity_provider_name,
                user=user
            )
            status_code = response.status_code
            json_data = response.json()
            
            log = {
                'email': user.email,
                'status_code': json_data,
            }

            if status_code != 201:
                log['message'] = json_data
            elif invite_users:

                # Invite existing user
                response = invite_existing_user(
                    token=self.token,
                    application_vanity_domain=self.application_vanity_domain,
                    tenant_id=self.tenant_id,
                    identity_provider_name=self.identity_provider_name,
                    user_id=json_data.get('id')
                )
                log['message'] = response.json()['existingUserInvitationRequest']['status']

                # Fetch roles
                if not did_fetch_roles:
                    roles = get_tenant_roles(
                        token=self.token,
                        application_vanity_domain=self.application_vanity_domain,
                        tenant_id=self.tenant_id
                    )
                    did_fetch_roles = True

                # Assign roles
                role_responses = []
                user_roles = user.roles.split(',') if isinstance(user.roles, str) else user.roles or []
                user_roles = [role.strip() for role in user_roles]  # Strip whitespace

                for role_name in user_roles:
                    # Find the matching role by displayName
                    matched_roles = [role for role in roles if role.get('displayName') == role_name]

                    if matched_roles:
                        response = assign_roles_to_user(
                            token=self.token,
                            application_vanity_domain=self.application_vanity_domain,
                            user_id=json_data.get('id'),
                            roles=matched_roles
                        )
                        role_responses.append(f"Role '{role_name}' added")
                    else:
                        role_responses.append(f"Role '{role_name}' not found")
                
                log['roles'] = role_responses

            logs.append(log)

        # Save logs to a CSV file
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if not os.path.exists('logs'):
            os.makedirs('logs')
        pd.DataFrame(logs).to_csv(f'logs/{timestamp}.csv', index=False)

        return logs
    
    def create_import_users_csv(self):
        """
        Creates an empty CSV file with the columns of the User model.
        """
        # Create a DataFrame

        df = pd.DataFrame(columns=User.fields())

        # Save the DataFrame to a CSV file
        df.to_csv(f'{self.import_file_path}', index=False)


    def get_import_users_from_csv(self) -> List[User]:
        """
        Reads a CSV file and parses it into a list of User objects.
        Throws a FileNotFoundError if the file does not exist.
        """
        # Check if the file exists
        if not os.path.exists(self.import_file_path):
            raise FileNotFoundError(f"The file '{self.import_file_path}' does not exist.")

        # Read the CSV file into a DataFrame
        df = pd.read_csv(self.import_file_path)

        users = []
        for _, row in df.iterrows():
            # Drop NaN values and convert the row to a dictionary
            user_data = row.dropna().to_dict()
            # Convert the dictionary to a User object
            user = User.from_dict(user_data)
            users.append(user)

        return users