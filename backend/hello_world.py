from fastapi import FastAPI
import psycopg2.extensions

app = FastAPI()
postgresql_db: psycopg2.extensions.connection

def create_app(connector: psycopg2.extensions.connection) -> FastAPI:
    
    global postgresql_db
    postgresql_db = connector
    
    return app

@app.get("/")
def read_root():
    
    cur = postgresql_db.cursor()
    cur.execute("SELECT version()")
    result = cur.fetchone()
    db_version: str = result[0] if result else "Unknown"
    cur.close()
    print("Database version:", db_version)
    # You can return the database version or any other info
    return {"message": "Hello World", "db_version": db_version}
