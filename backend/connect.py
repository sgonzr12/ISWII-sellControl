import psycopg2
from config import load_config

from typing import Optional
import psycopg2.extensions

class DatabaseConnection:
    _instance: Optional[psycopg2.extensions.connection] = None

    @classmethod
    def get_instance(cls) -> psycopg2.extensions.connection:
        if cls._instance is None:
            config = load_config()
            cls._instance = psycopg2.connect(
                dbname=config['dbname'],
                user=config['user'],
                password=config['password'],
                host=config['host'],
                port=config['port']
            )
        return cls._instance
    
    @classmethod
    def close_instance(cls) -> None:
        if cls._instance is not None:
            cls._instance.close()
            cls._instance = None

def get_db_connection() -> psycopg2.extensions.connection:
    return DatabaseConnection.get_instance()

def close_db_connection() -> None:
    DatabaseConnection.close_instance()