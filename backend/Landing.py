# Import necessary libraries
from fastapi import FastAPI
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os

# Start FastAPI app and configure session middleware
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key = os.getenv("FASTAPI_SECRET_KEY"))

# Load environment variables
load_dotenv(override=True)

# OAuth Setup
oauth = OAuth()
oauth.register(
    name = "google_oauth", # Unique name for the OAuth provider
    client_id = config("GOOGLE_CLIENT_ID"), # Google Client ID
    client_secret = config("GOOGLE_CLIENT_SECRET"), # Google Client Secret
    authorize_url = "https://accounts.google.com/o/oauth2/auth", # Redirect URL for Google authorization
    authorize_params = None, # Additional parameters for authorization above
    access_token_url = "https://accounts.google.com/o/oauth2/token", # Redirect URL for Google token exchange (after granted permission)
    access_token_params = None, # Additional parameters for token exchange above
    refresh_token_url = None, # Token refresh endpoint
    authorize_state = config("SECRET_KEY"), # (Optional) State parameter for CSRF protection
    redirect_uri = "http://127.0.0.1:8000/auth", # Redirect URL after successful login
    jwks_uri = "https://www.googleapis.com/oauth2/v3/certs", # JWKS URI for Google's public keys
    client_kwargs = {"scope": "openid profile email"}, # Permissions requested from Google
)

# JWT Configurations
SECRET_KEY = os.getenv("JWT_SECRET_KEY") 
ALGORITHM = "HS256" # Algorithm used for encoding/decoding JWT tokens