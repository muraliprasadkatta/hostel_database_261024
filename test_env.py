from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Print environment variables to confirm they're loaded
print("ALLOWED_HOSTS:", os.getenv("ALLOWED_HOSTS"))
print("SECRET_KEY:", os.getenv("SECRET_KEY"))
