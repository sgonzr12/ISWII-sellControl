import uvicorn
from fastapi import FastAPI
import os

from connect import get_db_connection, close_db_connection
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import backend.routers.user as user
import backend.routers.product as product

env_path = os.path.join(os.path.dirname(__file__), "../ps.env")
load_dotenv(env_path)
PORT = os.getenv("PORT")
FRONTEND_URL = os.getenv("FRONTEND_URL")


#TODO: change prints with logger (branch database)
if __name__ == "__main__":
    
    #open database connection
    connector = get_db_connection()

    #get app instance
    app = FastAPI()
    
    if FRONTEND_URL is None:
        raise ValueError("FRONTEND_URL environment variable not set")
    
    # TODO: change to allow only specific origins in production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[FRONTEND_URL],  # Allow all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )
    
    app.include_router(user.router, prefix="/user", tags=["user"])
    app.include_router(product.router, prefix="/product", tags=["product"])
    
    
    #change PORT to int
    if PORT is None:
        raise ValueError("PORT environment variable not set")
    
    #start the server
    uvicorn.run(app, host="0.0.0.0", port=int(PORT))
    
    #close database connection
    close_db_connection()

