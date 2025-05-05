from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
import jwt
import os
import requests

security = HTTPBearer()
    
# Load environment variables from .env file
load_dotenv()
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


def verifyToken(token: str = Depends(security))-> None:

    """
    Verify the token
    """

    # Verify loaded environment variables
    if CLIENT_ID is None or CLIENT_SECRET is None:
        raise HTTPException(status_code=500, detail="Missing environment variables")


    # Verify the token
    try:
        # Check the token with the Google API
        url = "https://oauth2.googleapis.com/tokeninfo?id_token=" + token
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
        user_info = response.json()
        if user_info.get("aud") != CLIENT_ID:
            raise HTTPException(status_code=401, detail="Token emitido para otra aplicacion")
        
        # Decode the token using the client ID and secret
        jwt.decode(token, CLIENT_SECRET, algorithms=["HS256"], audience=CLIENT_ID)
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    
def verifyUser(user_id: str, token: str = Depends(security)) -> None:
    """
    Verify that the user in request params matches the user in the token
    """
    # Decode the token to extract user information
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        token_user_id = payload.get("sub")  # Assuming "sub" contains the user ID
        if token_user_id != user_id:
            raise HTTPException(status_code=403, detail="User ID does not match the token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
