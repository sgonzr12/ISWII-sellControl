from fastapi import FastAPI
import psycopg2.extensions
import requests
from fastapi import HTTPException
import jwt
import datetime

app = FastAPI()
postgresql_db: psycopg2.extensions.connection

def create_app(connector: psycopg2.extensions.connection) -> FastAPI:
    
    global postgresql_db
    postgresql_db = connector
    
    return app

@app.get("/")
def read_root():
    
    cur = postgresql_db.cursor()
    cur.execute("SELECT version()")
    result = cur.fetchone()
    db_version: str = result[0] if result else "Unknown"
    cur.close()
    print("Database version:", db_version)
    # You can return the database version or any other info
    return {"message": "Hello World", "db_version": db_version}

    """
    endpoint to check a token with the google auth service
    Args:
        token (str): user token from google auth service

    Returns:
        access_token (str): access token for the user
    """
@app.get("/auth")
def auth(token: str) -> str:
    
    SECRET_KEY = "your_secret_key"  #TODO: replace with secret key and store it in a secure place 
    
    try:
        user_data = validate_google_token(token)
    except HTTPException as e:
        return "Authentication failed: " + str(e.detail)
    
    expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)

    payload = {
        "sub": str(user_data["sub"]),
        "email": str(user_data["email"]),
        "name": str(user_data["name"]),
        "rol": "0",  # TODO: implement roles
        "exp": expiration_time.isoformat(),  # Convert datetime to ISO 8601 string
    }

    access_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")  # type: ignore

    return access_token


def validate_google_token(id_token: str, google_client_id: str = "547605560322-uhhrg4hg9lccjnoica1oec7n0jcij1r9.apps.googleusercontent.com"):
    """
    Valida un id_token de Google y devuelve los datos del usuario si es válido.
    """
    url = "https://oauth2.googleapis.com/tokeninfo?id_token=" + id_token
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
    user_info = response.json()
    
    # Verificar que el token fue emitido para nuestro cliente
    if user_info.get("aud") != google_client_id:
        raise HTTPException(status_code=401, detail="Token emitido para otra aplicacion")
    
    return {
        "sub": user_info.get("sub"),  # ID único del usuario en Google
        "email": user_info.get("email"),
        "name": user_info.get("name"),
        "picture": user_info.get("picture"),
        "email_verified": user_info.get("email_verified"),
    }
