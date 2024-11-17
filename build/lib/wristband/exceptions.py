class AuthenticationError(Exception):
    """Custom exception for authentication failures."""
    pass

class AuthorizationError(Exception):
    """Custom exception for authorization failures."""
    pass

class BadRequestError(Exception):
    """Custom exception for bad request errors."""
    pass
