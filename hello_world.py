from fastapi import FastAPI

app = FastAPI()

def create_app():
    return app

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
