import uvicorn
from fastapi import FastAPI

from connect import get_db_connection, close_db_connection
from fastapi.middleware.cors import CORSMiddleware
import user




#TODO: change prints with logger (branch database)
if __name__ == "__main__":
    
    #open database connection
    connector = get_db_connection()

    #get app instance
    app = FastAPI()
    
    # TODO: change to allow only specific origins in production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )
    
    app.include_router(user.router, prefix="user", tags=["user"])
    
    #start the server
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    #close database connection
    close_db_connection()
    



user_instance = user