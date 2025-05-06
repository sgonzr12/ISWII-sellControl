from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials 
from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import jwt
import os

security = HTTPBearer()
    
# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), "../ps.env")

load_dotenv(env_path)
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


def verifyToken(token: HTTPAuthorizationCredentials = Depends(security)) -> dict[str, str]:
    """
    Verify the token
    """
    
    print("Verifying token")  # TODO: REMOVE WHEN LOGGER IS READY

    credentials = token.credentials  # Extract the actual token string

    # Verify loaded environment variables
    if CLIENT_ID is None or CLIENT_SECRET is None:
        raise HTTPException(status_code=500, detail="Missing environment variables")

    # Verify the token
    try:
        decoded_token = id_token.verify_oauth2_token( #type: ignore
            credentials,
            request=google_requests.Request(),
            audience=CLIENT_ID
        )
        return decoded_token
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
