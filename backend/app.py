from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials 
from dotenv import load_dotenv
import jwt
import os
import requests

security = HTTPBearer()
    
# Load environment variables from .env file
load_dotenv("../ps.env")
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


def verifyToken(token: HTTPAuthorizationCredentials = Depends(security)) -> None:
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
        # Check the token with the Google API
        url = "https://oauth2.googleapis.com/tokeninfo?id_token=" + credentials
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
        user_info = response.json()
        if user_info.get("aud") != CLIENT_ID:
            raise HTTPException(status_code=401, detail="Token emitido para otra aplicacion")
        
        # Decode the token using the client ID and secret
        jwt.decode(credentials, CLIENT_SECRET, algorithms=["HS256"], audience=CLIENT_ID)
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
