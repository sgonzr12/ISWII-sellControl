import uvicorn
import logging

from config import load_config
from connect import connect
from hello_world import create_app

if __name__ == "__main__":
    
    # Set up logging
    logger = logging.getLogger("appLogger")
    logger.setLevel(logging.DEBUG)
    
    # Load the database configurationç
    config = load_config()
    
    # Connect to the PostgreSQL database
    postgreesql_db = connect(config)
    
    if postgreesql_db is None:
        raise ValueError("Database connection failed.")
    app = create_app(postgreesql_db)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)