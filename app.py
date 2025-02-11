from fastapi import FastAPI
import openai
from dotenv import load_dotenv
import os


####### OPEN AI init ########
openai.api_key = os.getenv("api_key")


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
