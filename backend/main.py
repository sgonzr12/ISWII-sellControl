import uvicorn

from config import load_config
from connect import connect
from hello_world import create_app



if __name__ == "__main__":
    
    # Load the database configuration
    config = load_config()
    postgreesql_db = connect(config)
    
    if postgreesql_db is None:
        raise ValueError("Database connection failed.")
    app = create_app(postgreesql_db)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
