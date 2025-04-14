# Import necessary libraries
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, Depends
import requests
import jwt

# Configuration values for Google OAuth2
GOOGLE_CLIENT_ID = "your_google_client_id"
GOOGLE_CLIENT_SECRET = "your_google_client_secret"
GOOGLE_REDIRECT_URI = "http://localhost:8000/auth/google/callback"

'''
    Route for Google Login:
    Returns a URL to redirect the user to Google's OAuth login page.
    TODO: Change the redirect URI to the frontend URL when deploying.
'''
@app.get("../frontend/src/GoogleLogin.tsx")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }

'''
    Route for Google Callback:
    Handles the callback from Google after user authentication.
    Exchanges the authorization code for an access token and retrieves the user's information.
    TODO: Change the redirect URI to the frontend URL when deploying.
'''
@app.get("../frontend/src/GoogleCallback.tsx")
async def auth_google(code: str):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    return user_info.json()

'''
    Route for Decoding JWT Token:
    Decodes the JWT token received from Google after user authentication.
    TODO: Change the redirect URI to the frontend URL when deploying.
'''
@app.get("../frontend/src/GoogleToken.tsx")
async def get_token(token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, GOOGLE_CLIENT_SECRET, algorithms=["HS256"])