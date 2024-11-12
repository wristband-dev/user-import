import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from exceptions import AuthenticationError, AuthorizationError, BadRequestError
import math

class service:
    def __init__(self, token, application_vanity_domain, tenant_id, identity_provider_name):
        self.token = token
        self.application_vanity_domain = application_vanity_domain
        self.tenant_id = tenant_id
        self.identity_provider_name = identity_provider_name

        self.input_file_name = 'input_user.csv'
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
        

    def create_user(
        self,
        user_fields: dict
    ):
        # Construct the URL
        url = f'https://{self.application_vanity_domain}/api/v1/users'

        # Headers to indicate the type of data being sent
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json',
            'authorization': f'Bearer {self.token}',
        }

        querystring = {
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
                querystring[field] = user_fields[field]

        print(querystring)

        # Perform the GET request
        response = requests.post(url, headers=headers, json=querystring)

        if response.status_code == 404:
            raise BadRequestError("ApplicationId is not valid - please rerun script & enter a valid applicationId")
        elif response.status_code == 403:
            raise AuthorizationError("Client is not authorized to perform the user export - please make sure that the client has the appropriate permissions assigned to it and then rerun script")

        # Return response
        return response
    

    def create_input_user_csv(self):
        # Create a DataFrame with the allowed user fields as columns
        df = pd.DataFrame(columns=self.allowed_user_fields)

        # Save the DataFrame to a CSV file
        df.to_csv(f'{self.input_file_name}.csv', index=False)


    def get_user_fields_from_csv(self):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(f'{self.input_file_name}.csv')

        # Convert the DataFrame to a dictionary
        user_fields = df.to_dict(orient='records')

        return user_fields