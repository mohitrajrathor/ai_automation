import subprocess
import os
from datetime import datetime
import json
import sqlite3

import pytesseract
from PIL import Image
import openai
import numpy as np

########## CONST ##########
DATA_DIR = "/data"


def format_markdown(file_path: str):
    """Formats a Markdown file using Prettier"""
    full_path = os.path.join(DATA_DIR, file_path.lstrip("/"))
    subprocess.run(["npx", "prettier", "--write", full_path], check=True)
    return {"message": "Markdown formatted"}


def install_and_run_script(user_email: str):
    """Installs `uv` if needed and runs `datagen.py`"""
    subprocess.run(["pip", "install", "uv"], check=True)
    subprocess.run(
        ["python", "-m", "uv", "pip", "install", "-r", "requirements.txt"], check=True
    )
    subprocess.run(["python", "datagen.py", user_email], check=True)
    return {"message": "Data generation complete"}


def count_wednesdays(file_path: str, output_path: str):
    """Counts the number of Wednesdays in a date file"""
    full_path = os.path.join(DATA_DIR, file_path.lstrip("/"))
    output_full_path = os.path.join(DATA_DIR, output_path.lstrip("/"))

    with open(full_path, "r") as f:
        dates = [
            datetime.strptime(line.strip(), "%Y-%m-%d") for line in f if line.strip()
        ]

    wednesdays = sum(1 for date in dates if date.weekday() == 2)

    with open(output_full_path, "w") as f:
        f.write(str(wednesdays))

    return {"message": f"Counted {wednesdays} Wednesdays"}


def sort_contacts(file_path: str, output_path: str):
    """Sorts a JSON array of contacts by last_name, then first_name"""
    full_path = os.path.join(DATA_DIR, file_path.lstrip("/"))
    output_full_path = os.path.join(DATA_DIR, output_path.lstrip("/"))

    with open(full_path, "r") as f:
        contacts = json.load(f)

    contacts.sort(key=lambda c: (c["last_name"], c["first_name"]))

    with open(output_full_path, "w") as f:
        json.dump(contacts, f, indent=2)

    return {"message": "Contacts sorted"}


def extract_recent_logs(directory: str, output_path: str):
    """Extracts the first line of the 10 most recent log files"""
    log_files = sorted(
        [f for f in os.listdir(directory) if f.endswith(".log")],
        key=lambda x: os.path.getmtime(os.path.join(directory, x)),
        reverse=True,
    )[:10]

    first_lines = []
    for file in log_files:
        with open(os.path.join(directory, file), "r") as f:
            first_lines.append(f.readline().strip())

    with open(output_path, "w") as f:
        f.write("\n".join(first_lines))

    return {"message": "Recent logs extracted"}


def extract_markdown_titles(directory: str, output_path: str):
    """Extracts H1 titles from Markdown files in a directory"""
    index = {}

    for file in os.listdir(directory):
        if file.endswith(".md"):
            with open(os.path.join(directory, file), "r") as f:
                for line in f:
                    if line.startswith("# "):
                        index[file] = line[2:].strip()
                        break  # Only first H1

    with open(output_path, "w") as f:
        json.dump(index, f, indent=2)

    return {"message": "Markdown titles extracted"}


def calculate_sales(db_file: str, output_path: str):
    """Calculates the total sales for 'Gold' ticket type"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
    total_sales = cursor.fetchone()[0] or 0

    with open(output_path, "w") as f:
        f.write(str(total_sales))

    conn.close()
    return {"message": f"Total Gold ticket sales: {total_sales}"}


import openai


def extract_email_sender(input_file: str, output_file: str):
    """
    Reads an email from a file, extracts the sender’s email address using an LLM, and writes it to an output file.

    Parameters:
    - input_file (str): Path to the email text file.
    - output_file (str): Path where the extracted email address will be saved.
    """

    # Read email content
    with open(input_file, "r", encoding="utf-8") as f:
        email_content = f.read()

    # Prompt for the LLM
    prompt = f"""
    You are an expert in extracting email metadata. Given an email message, extract the sender’s email address.

    Email Message:
    {email_content}

    Respond strictly with just the email address.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You extract sender email addresses from emails.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    sender_email = response["choices"][0]["message"]["content"].strip()

    # Write extracted email to output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(sender_email)

    return sender_email


def extract_credit_card(input_file: str, output_file: str):
    """
    Reads a credit card number from an image file using OCR and saves it without spaces.

    Parameters:
    - input_file (str): Path to the image containing the credit card number.
    - output_file (str): Path where the extracted number will be saved.
    """

    # Load the image
    image = Image.open(input_file)

    # Extract text using OCR
    extracted_text = pytesseract.image_to_string(image)

    # Filter out digits only (removing spaces and other non-numeric characters)
    credit_card_number = "".join(filter(str.isdigit, extracted_text))

    # Write to output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(credit_card_number)

    return credit_card_number


def find_similar_comments(input_file: str, output_file: str):
    """
    Finds the most similar pair of comments in a file using embeddings and writes them to an output file.

    Parameters:
    - input_file (str): Path to the file containing comments (one per line).
    - output_file (str): Path where the most similar comments will be saved.
    """

    # Read comments from file
    with open(input_file, "r", encoding="utf-8") as f:
        comments = [line.strip() for line in f.readlines() if line.strip()]

    # Get embeddings for each comment
    embeddings = []
    for comment in comments:
        response = openai.Embedding.create(
            model="text-embedding-ada-002", input=comment
        )
        embeddings.append(np.array(response["data"][0]["embedding"]))

    # Find the most similar pair
    min_distance = float("inf")
    most_similar_pair = ("", "")

    for i in range(len(comments)):
        for j in range(i + 1, len(comments)):
            distance = np.linalg.norm(
                embeddings[i] - embeddings[j]
            )  # Euclidean distance
            if distance < min_distance:
                min_distance = distance
                most_similar_pair = (comments[i], comments[j])

    # Write the most similar comments to output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(most_similar_pair[0] + "\n" + most_similar_pair[1])

    return most_similar_pair
