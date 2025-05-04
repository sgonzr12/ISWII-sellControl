import uvicorn

from config import load_config
from connect import connect
from hello_world import create_app


#TODO: change prints with logger (branch database)
if __name__ == "__main__":
    
    # Load the database configuration
    config = load_config("../database.ini", "postgresql")
    print("Database configuration loaded:", config)
    postgresql_db = connect(config)
    print("Database connection established.")
    
    if postgresql_db is None:
        raise ValueError("Database connection failed.")
    app = create_app(postgresql_db)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
