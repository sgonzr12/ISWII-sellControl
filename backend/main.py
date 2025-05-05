import uvicorn
from fastapi import FastAPI

from connect import get_db_connection, close_db_connection
from fastapi.middleware.cors import CORSMiddleware

_app_instance = None


def get_app() -> FastAPI:
    global _app_instance
    if _app_instance is None:
        _app_instance = FastAPI()
    return _app_instance





#TODO: change prints with logger (branch database)
if __name__ == "__main__":
    
    #open database connection
    connector = get_db_connection()

    #get app instance
    app = get_app()
    
    # TODO: change to allow only specific origins in production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )
    
    #start the server
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    #close database connection
    close_db_connection()
    



