import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from wristband.exceptions import AuthenticationError, AuthorizationError, BadRequestError
import math
from datetime import datetime
import os

class UsersService:
    def __init__(self, token=None, application_vanity_domain=None, tenant_id=None, identity_provider_name=None):
        self.token = token
        self.application_vanity_domain = application_vanity_domain
        self.tenant_id = tenant_id
        self.identity_provider_name = identity_provider_name

        self.input_file_name = 'input_users.csv'
        self.allowed_user_fields  = [
            'username',
            'password',
            'email',
            'emailVerified',
            'externalId',
            'fullName',
            'givenName',
            'familyName',
            'middleName',
            'honorificPrefix',
            'honorificSuffix',
            'nickname',
            'displayName',
            'pictureUrl',
            'gender',
            'birthdate',
            'phoneNumber',
            'preferredLanguage',
            'locale',
            'timeZone'
        ]

    def upload_users_csv(
        self,
        invite_users = True
    ): 
        # Initialize log
        logs = []

        # Get users
        users = self.get_input_users_from_csv()
        for user in users:
            create_user_response = self.create_user(user_fields=user)
            status_code = create_user_response.status_code
            response_json = create_user_response.json()
            
            log = {
                'email': user.get('email'),
                'status_code': status_code,
            }

            if status_code != 201:
                log['message'] = response_json
            elif invite_users:
                invite_exisiting_user_response = self.invite_existing_user(user_id=response_json.get('id'))
                log['message'] = invite_exisiting_user_response.json()['existingUserInvitationRequest']['status']

            logs.append(log)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if not os.path.exists('logs'):
            os.makedirs('logs')
        pd.DataFrame(logs).to_csv(f'logs/{timestamp}.csv', index=False)
        return logs
    
    def create_user(
        self,
        user_fields: dict
    ):
        """
        API Docs - https://docs.wristband.dev/reference/createuserv1
        """
        if not self.token or not self.application_vanity_domain or not self.tenant_id or not self.identity_provider_name:
            raise BadRequestError("Service is not properly initialized with required credentials.")

        # Construct the URL
        url = f'https://{self.application_vanity_domain}/api/v1/users'

        # Headers to indicate the type of data being sent
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json',
            'authorization': f'Bearer {self.token}',
        }

        request_body = {
            'tenantId': self.tenant_id,
            'identityProviderName': self.identity_provider_name,
        }

        # Check if the user_fields contain any invalid fields
        for field in user_fields.keys():
            if field not in self.allowed_user_fields:
                raise BadRequestError(f"Invalid field: {field}")
            elif isinstance(user_fields[field], float) and math.isnan(user_fields[field]):
                continue  # Skip adding fields with NaN values
            else:
                request_body[field] = user_fields[field]

        # Perform the GET request
        response = requests.post(url, headers=headers, json=request_body)

        if response.status_code == 404:
            raise BadRequestError("ApplicationId is not valid - please rerun script & enter a valid applicationId")
        elif response.status_code == 403:
            raise AuthorizationError("Client is not authorized to perform the user export - please make sure that the client has the appropriate permissions assigned to it and then rerun script")

        # Return response
        return response
    
    def invite_existing_user(
        self,
        user_id: str
    ):
        """
        API Docs - https://docs.wristband.dev/reference/inviteexistinguserv1
        """
        if not self.token or not self.application_vanity_domain or not self.tenant_id or not self.identity_provider_name:
            raise BadRequestError("Service is not properly initialized with required credentials.")

        # Construct the URL
        url = f'https://{self.application_vanity_domain}/api/v1/existing-user-invitation/invite-user'

        # Headers to indicate the type of data being sent
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json',
            'authorization': f'Bearer {self.token}',
        }

        # Construct the request body
        request_body = {
            'userId': user_id
        }

        # Perform the POST request with JSON payload
        response = requests.post(url, headers=headers, json=request_body)

        if response.status_code == 404:
            raise BadRequestError("ApplicationId is not valid - please rerun script & enter a valid applicationId")
        elif response.status_code == 403:
            raise AuthorizationError("Client is not authorized to perform the user export - please make sure that the client has the appropriate permissions assigned to it and then rerun script")

        # Return response
        return response          
        
    def create_input_users_csv(self):
        # Create a DataFrame with the allowed user fields as columns
        df = pd.DataFrame(columns=self.allowed_user_fields)

        # Save the DataFrame to a CSV file
        df.to_csv(f'{self.input_file_name}.csv', index=False)

    def get_input_users_from_csv(self):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(f'{self.input_file_name}.csv')

        # Convert the DataFrame to a dictionary
        user_fields = df.to_dict(orient='records')

        return user_fields