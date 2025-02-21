import uvicorn
from fastapi import FastAPI
import openai
from dotenv import load_dotenv
import os
from fastapi import HTTPException
from phase_A import *
from prompt import parse_task_with_llm


####### OPEN AI init ########
openai.api_key = os.environ["AIPROXY_TOKEN"]

######## INIT ########
app = FastAPI()


######## CONST ########
DATA_DIR = "/data"


######## Routes #########
@app.get("/read")
def read(path: str):
    """Reads a file's contents from the /data directory."""
    full_path = os.path.join(DATA_DIR, path.lstrip("/"))
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(full_path, "r", encoding="utf-8") as f:
        return {"content": f.read()}


@app.post("/run")
def run(task: str):
    """
    route to perform a task
    """
    """ Parses and executes a given task. """
    # Call GPT-4o-Mini to interpret the task
    action, params = parse_task_with_llm(task)

    # Execute the required function based on the action
    try:
        if action == "install_and_run":
            return install_and_run_script(params["email"])
        elif action == "format_markdown":
            return format_markdown(params["file"])
        elif action == "count_wednesdays":
            return count_wednesdays(params["file"], params["output"])
        elif action == "sort_contacts":
            return sort_contacts(params["file"], params["output"])
        elif action == "extract_recent_logs":
            return extract_recent_logs(params["dir"], params["output"])
        elif action == "extract_markdown_titles":
            return extract_markdown_titles(params["dir"], params["output"])
        elif action == "extract_email_sender":
            return extract_email_sender(params["file"], params["output"])
        elif action == "extract_credit_card":
            return extract_credit_card(params["file"], params["output"])
        elif action == "find_similar_comments":
            return find_similar_comments(params["file"], params["output"])
        elif action == "calculate_sales":
            return calculate_sales(params["db_file"], params["output"])
        else:
            return {"error": "Unknown task"}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
