import uuid
from datetime import timedelta
from django.utils.timezone import now

def generate_token():
    """
    Generates a unique token for password reset.
    
    Returns:
        str: A unique token as a string.
    """
    return str(uuid.uuid4())

def is_token_valid(token_creation_time):
    """
    Checks if the token is still valid based on a predefined expiration time.
    
    Args:
        token_creation_time (datetime): The time the token was created.
    
    Returns:
        bool: True if the token is valid, False otherwise.
    """
    expiration_time = timedelta(hours=1)  # Token validity period
    return now() - token_creation_time <= expiration_time
