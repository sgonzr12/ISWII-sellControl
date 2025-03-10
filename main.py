import uvicorn
from hello_world import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("hello_world:app", host="0.0.0.0", port=8000, reload=True)
