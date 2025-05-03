import psycopg2
from config import load_config

from typing import Optional
import psycopg2.extensions

def connect(config: dict[str, str]) -> Optional[psycopg2.extensions.connection]:
    """ Connect to the PostgreSQL database server """
    try:
        print('Connecting to the PostgreSQL database...')
        # connecting to the PostgreSQL server
        with psycopg2.connect(
            dbname=config.get("database"),
            user=config.get("user"),
            password=config.get("password"),
            host=config.get("host"),
            port=config.get("port")
        ) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == '__main__':
    config = load_config()
    connect(config)