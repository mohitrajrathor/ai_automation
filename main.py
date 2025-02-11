import uvicorn
from fastapi import FastAPI
import openai
from dotenv import load_dotenv
import os


####### OPEN AI init ########
openai.api_key = os.getenv("AIPROXY_TOKEN")


######## INIT ########
app = FastAPI()


######## Routes #########
@app.get("/")
def index():
    try:
        return {"message": "Hello, JSON!"}
    except Exception as e:
        print(e)
        return "Error"


@app.get("/read")
def read(path: str):
    """
    route to read files
    """
    try:

        # TODO:
        # 1. read project

        return {"path": path}
    except Exception as e:
        print("Error", e)
        return {"error": "internal server error"}


@app.post("/run")
def run(task: str):
    """
    route to perform a task
    """
    try:
        return {"task": task}
    except Exception as e:
        print("Error", e)
        return {"error": "internal server error"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
