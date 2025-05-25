import psycopg2
import os
from dotenv import load_dotenv

from typing import Optional
import psycopg2.extensions

env_path = os.path.join(os.path.dirname(__file__), "../ps.env")
load_dotenv(env_path)

DATABASE = os.getenv("DATABASE_NAME")
if not DATABASE:
    raise ValueError("DATABASE_NAME environment variable not set")
USER = os.getenv("DATABASE_USER")
if not USER:
    raise ValueError("DATABASE_USER environment variable not set")
PASSWORD = os.getenv("DATABASE_PASSWORD")
if not PASSWORD:
    raise ValueError("DATABASE_PASSWORD environment variable not set")
HOST = os.getenv("DATABASE_URL")
if not HOST:
    raise ValueError("DATABASE_HOST environment variable not set")

class DatabaseConnection:
    _instance: Optional[psycopg2.extensions.connection] = None

    @classmethod
    def get_instance(cls) -> psycopg2.extensions.connection:
        if cls._instance is None:
            cls._instance = psycopg2.connect(
                dbname=DATABASE,
                user=USER,
                password=PASSWORD,
                host=HOST
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