import uvicorn
import logging

from config import load_config
from connect import connect
from hello_world import create_app
from main import Logger

if __name__ == "__main__":
    
    # Set up logging
    logger = Logger().get_logger()
    logger.info("Starting the application...")
    
    # Load the database configurationç
    
    config = load_config()
    postgreesql_db = connect(config)
    
    if postgreesql_db is None:
        raise ValueError("Database connection failed.")
    app = create_app(postgreesql_db)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    class Logger:
        _instance = None
        _logger = None

        def __new__(cls):
            if cls._instance is None:
                cls._logger = logging.getLogger("AppLogger")
                cls._logger.setLevel(logging.INFO)
                handler = logging.StreamHandler()
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                cls._logger.addHandler(handler)
            return cls._instance

        def get_logger(self) -> logging.Logger:
                
            if self._logger is None:
                raise ValueError("Logger instance is not initialized.")
            return self._logger