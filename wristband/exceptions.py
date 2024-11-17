class AuthenticationError(Exception):
    """Custom exception for authentication failures."""
    pass

class AuthorizationError(Exception):
    """Custom exception for authorization failures."""
    pass

class BadRequestError(Exception):
    """Custom exception for bad request errors."""
    pass

def get_non_empty_response(prompt):
    """Prompt the user until a non-empty response is given."""
    while True:
        response = input(prompt)
        if response.strip():
            return response
        else:
            print("This field cannot be empty. Please try again.")
