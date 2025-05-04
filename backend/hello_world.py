from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Callable, Awaitable
import psycopg2.extensions
import requests
import jwt
import datetime


app = FastAPI()
postgresql_db: psycopg2.extensions.connection

# Configure CORS TODO: change to allow only specific origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development purposes
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

def create_app(connector: psycopg2.extensions.connection) -> FastAPI:
    global postgresql_db
    global SECRET_KEY
    postgresql_db = connector
    SECRET_KEY = "b]ORCQ0{mp+<h7s)3|("  # TODO: replace with secret key and store it in a secure place
    return app

# Middleware that checks JWT for all routes    
@app.middleware("http")
async def verifyTOken(request: Request, call_next: Callable[[Request], Awaitable[JSONResponse]])-> JSONResponse:
    # Exclude authentication for certain paths
    if request.url.path in ["/auth", ]:
        return await call_next(request)
    
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return JSONResponse(status_code=401, content={"detail": "Authentication required"})
      
    try:
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            return JSONResponse(status_code=401, content={"detail": "Invalid authentication scheme"})
            
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
           
        # Check if token is expired
        exp_value = payload.get("exp")
        if isinstance(exp_value, str):
            expiration = datetime.datetime.fromisoformat(exp_value)
            if expiration < datetime.datetime.now(datetime.timezone.utc):
                return JSONResponse(status_code=401, content={"detail": "Token has expired"})
            
        # Add user info to request state for access in endpoint handlers
        request.state.user = payload
           
        return await call_next(request)
    except Exception:
        return JSONResponse(status_code=401, content={"detail": "Invalid authentication credentials"})
    

@app.get("/" )
def read_root():
    cur = postgresql_db.cursor()
    cur.execute("SELECT version()")
    result = cur.fetchone()
    db_version: str = result[0] if result else "Unknown"
    cur.close()
    print("Database version:", db_version)
    return {"message": "Hello World", "db_version": db_version}

@app.post("/auth")
async def auth(google_token: dict[str, str])-> dict[str, str|bytes]:
    try:
        user_data = await validate_google_token(google_token["token"])
    except HTTPException as exception:
        raise exception

    expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)

    payload: dict[str,str] = {
        "sub": str(user_data["sub"]),
        "email": str(user_data["email"]),
        "name": str(user_data["name"]),
        "rol": "0",  # TODO: implement roles
        "exp": str(expiration_time.timestamp())  # Add expiration as timestamp
    }

    access_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    # Return the token along with metadata
    return {"access_token": access_token, "token_type": "bearer"}


    
    

async def validate_google_token(id_token: str, google_client_id: str = "547605560322-uhhrg4hg9lccjnoica1oec7n0jcij1r9.apps.googleusercontent.com"):
    url = "https://oauth2.googleapis.com/tokeninfo?id_token=" + id_token
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    user_info = response.json()
    if user_info.get("aud") != google_client_id:
        raise HTTPException(status_code=401, detail="Token emitido para otra aplicacion")
    return {
        "sub": user_info.get("sub"),
        "email": user_info.get("email"),
        "name": user_info.get("name"),
        "picture": user_info.get("picture"),
        "email_verified": user_info.get("email_verified"),
    }
