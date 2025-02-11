import os
import subprocess
import json
import re
import sqlite3
from datetime import datetime
from collections import defaultdict
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load AI Proxy Token
aiproxy_token = os.getenv("AIPROXY_TOKEN")
client = OpenAI(api_key=aiproxy_token)


temo = {}


# Task A1: Install uv and run datagen.py
def task_a1(user_email):
    subprocess.run(["pip", "install", "uv"], check=True)
    subprocess.run(["python", "datagen.py", user_email], check=True)


# Task A2: Format /data/format.md using prettier@3.4.2
def task_a2():
    subprocess.run(["npx", "prettier@3.4.2", "--write", "/data/format.md"], check=True)


# Task A3: Count Wednesdays in /data/dates.txt
def task_a3():
    with open("/data/dates.txt", "r") as f:
        dates = f.readlines()
    count = sum(
        1
        for date in dates
        if datetime.strptime(date.strip(), "%Y-%m-%d").weekday() == 2
    )
    with open("/data/dates-wednesdays.txt", "w") as f:
        f.write(str(count))


# Task A4: Sort contacts by last_name, first_name
def task_a4():
    with open("/data/contacts.json", "r") as f:
        contacts = json.load(f)
    contacts.sort(key=lambda x: (x["last_name"], x["first_name"]))
    with open("/data/contacts-sorted.json", "w") as f:
        json.dump(contacts, f, indent=2)


# Task A5: Get first line of 10 most recent .log files
def task_a5():
    logs = sorted(Path("/data/logs").glob("*.log"), key=os.path.getmtime, reverse=True)[
        :10
    ]
    with open("/data/logs-recent.txt", "w") as f:
        for log in logs:
            with open(log, "r") as log_file:
                f.write(log_file.readline())


# Task A6: Extract H1 titles from Markdown files
def task_a6():
    index = {}
    for md_file in Path("/data/docs").glob("*.md"):
        with open(md_file, "r") as f:
            for line in f:
                if line.startswith("# "):
                    index[md_file.name] = line.strip("# ").strip()
                    break
    with open("/data/docs/index.json", "w") as f:
        json.dump(index, f, indent=2)


# Task A7: Extract sender email from email.txt using LLM
def task_a7():
    with open("/data/email.txt", "r") as f:
        email_content = f.read()
    response = client.completions.create(
        model="gpt-4o-mini",
        prompt=f"Extract the sender's email from this message:\n{email_content}\nOnly return the email address.",
        max_tokens=50,
    )
    sender_email = response.choices[0].text.strip()
    with open("/data/email-sender.txt", "w") as f:
        f.write(sender_email)


# Task A8: Extract credit card number from image using OCR/LLM
def task_a8():
    response = client.completions.create(
        model="gpt-4o-mini",
        prompt="Extract the credit card number from the image /data/credit-card.png. Return only the number without spaces.",
        max_tokens=50,
    )
    card_number = response.choices[0].text.strip()
    with open("/data/credit-card.txt", "w") as f:
        f.write(card_number)


# Task A9: Find most similar comments using embeddings
def task_a9():
    with open("/data/comments.txt", "r") as f:
        comments = f.readlines()
    embeddings = {
        comment: client.embeddings.create(
            input=comment, model="text-embedding-ada-002"
        ).data
        for comment in comments
    }
    most_similar = sorted(
        [
            (c1, c2, sum((a - b) ** 2 for a, b in zip(e1, e2)))
            for c1, e1 in embeddings.items()
            for c2, e2 in embeddings.items()
            if c1 != c2
        ],
        key=lambda x: x[2],
    )[0][:2]
    with open("/data/comments-similar.txt", "w") as f:
        f.write("\n".join(most_similar))


# Task A10: Sum ticket sales for "Gold" tickets in SQLite
def task_a10():
    conn = sqlite3.connect("/data/ticket-sales.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type='Gold'")
    total_sales = cursor.fetchone()[0] or 0
    conn.close()
    with open("/data/ticket-sales-gold.txt", "w") as f:
        f.write(str(total_sales))


# Example: Running a Task
def run_task(task_id):
    tasks = {
        "A1": lambda: task_a1(os.getenv("email")),
        "A2": task_a2,
        "A3": task_a3,
        "A4": task_a4,
        "A5": task_a5,
        "A6": task_a6,
        "A7": task_a7,
        "A8": task_a8,
        "A9": task_a9,
        "A10": task_a10,
    }
    if task_id in tasks:
        tasks[task_id]()
        print(f"Task {task_id} completed.")
    else:
        print("Invalid task ID")


func_obj = {""}


# Example Usage
if __name__ == "__main__":
    run_task("A3")
