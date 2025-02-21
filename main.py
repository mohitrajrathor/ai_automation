import uvicorn
from fastapi import FastAPI, HTTPException
import openai
from dotenv import load_dotenv
import os

# Importing functions
from phase_A import (
    install_and_run_script,
    format_markdown,
    count_wednesdays,
    sort_contacts,
    extract_recent_logs,
    extract_markdown_titles,
    extract_email_sender,
    extract_credit_card,
    find_similar_comments,
    calculate_sales,
)
from prompt import parse_task_with_llm

# Load environment variables
load_dotenv()

# Initialize OpenAI API key
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
if not AIPROXY_TOKEN:
    raise ValueError("AIPROXY_TOKEN is not set in the environment variables.")
openai.api_key = AIPROXY_TOKEN

# Initialize FastAPI app
app = FastAPI()

# Constants
DATA_DIR = "/data"


@app.get("/read")
def read(path: str):
    """Reads a file's contents from the /data directory."""
    full_path = os.path.join(os.getcwd(), DATA_DIR, path.lstrip("/"))
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(full_path, "r", encoding="utf-8") as f:
        return {"content": f.read()}


@app.post("/run")
def run(task: str):
    """Parses and executes a given task using GPT-4o-Mini."""
    try:
        action, params = parse_task_with_llm(task)

        task_mapping = {
            "install_and_run": lambda: install_and_run_script(params["email"]),
            "format_markdown": lambda: format_markdown(params["file"]),
            "count_wednesdays": lambda: count_wednesdays(
                params["file"], params["output"]
            ),
            "sort_contacts": lambda: sort_contacts(params["file"], params["output"]),
            "extract_recent_logs": lambda: extract_recent_logs(
                params["dir"], params["output"]
            ),
            "extract_markdown_titles": lambda: extract_markdown_titles(
                params["dir"], params["output"]
            ),
            "extract_email_sender": lambda: extract_email_sender(
                params["file"], params["output"]
            ),
            "extract_credit_card": lambda: extract_credit_card(
                params["file"], params["output"]
            ),
            "find_similar_comments": lambda: find_similar_comments(
                params["file"], params["output"]
            ),
            "calculate_sales": lambda: calculate_sales(
                params["db_file"], params["output"]
            ),
        }

        if action in task_mapping:
            return task_mapping[action]()
        return {"error": "Unknown task"}

    except Exception as e:
        print(e)
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
