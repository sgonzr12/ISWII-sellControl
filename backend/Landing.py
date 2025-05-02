# Import necessary libraries
from fastapi import FastAPI, HTTPException, Cookie, Request,
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from jose import jwt, ExpiredSignatureError, JWTError
from fastapi.responses import RedirectResponse


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

# Encode Secret Key into a JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days = 1))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Extracts token from Cookie and decodes it to get user information
def get_current_user(token: str = Cookie(None)):
    if not token:
        raise HTTPException(status_code = 401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"user_id": payload.get("sub"), "email": payload.get("email")}
    except ExpiredSignatureError:
        raise HTTPException(status_code = 401, detail = "Token expired")
    except JWTError:
        raise HTTPException(status_code = 401, detail = "Invalid token")
    
@router.get("/login")
async def login(request: Request):
    request.session.clear()
    frontend_url = os.getenv("FRONTEND_URL")
    redirect_url = os.getenv("REDIRECT_URL")
    request.session["login_redirect"] = frontend_url 

    return await oauth.auth_demo.authorize_redirect(request, redirect_url, prompt = "consent")

@router.route("/auth")
async def auth(request: Request):
    try:
        # Exchange the authorization code from Google consent for an access token
        token = await oauth.auth_demo.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code = 401, detail = "Google authentication failed.")

    try:
        user_info_endpoint = "https://www.googleapis.com/oauth2/v2/userinfo" # Endpoint to get user information
        headers = {"Authorization": f'Bearer {token["access_token"]}'} # Uses the token to access this
        google_response = requests.get(user_info_endpoint, headers=headers)
    except Exception as e:
        raise HTTPException(status_code = 401, detail = "Google authentication failed.")

    user = token.get("userinfo")
    expires_in = token.get("expires_in")
    user_id = user.get("sub")
    iss = user.get("iss") # Issuer (Google)
    user_email = user.get("email")

    # Check to see if the token was issued from Google (Prevent token forgery)
    if iss not in ["https://accounts.google.com", "accounts.google.com"]:
        raise HTTPException(status_code = 401, detail = "Google authentication failed.")

    if user_id is None:
        raise HTTPException(status_code = 401, detail = "Google authentication failed.")

    # Create JWT token
    access_token_expires = timedelta(seconds = expires_in)
    access_token = create_access_token(data = {"sub": user_id, "email": user_email}, expires_delta = access_token_expires)

    redirect_url = request.session.pop("login_redirect", "")
    response = RedirectResponse(redirect_url) # Redirect to the inicial page after login
    response.set_cookie(
        key = "access_token",
        value = access_token,
        httponly = True, # Prevents JS access to the cookie
        secure = True,  # Ensure Cookie is sent over HTTPS
        samesite = "strict",  # Sends the cookie only to the same site
    )

    return response