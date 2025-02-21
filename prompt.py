import os
import json
from openai import OpenAI
from dotenv import load_dotenv


def parse_task_with_llm(task: str):
    """
    Uses GPT-4o-Mini to analyze the task description and determine the action and parameters.

    Returns:
        dict: Parsed action and parameters.
    """
    load_dotenv()

    api_key = os.getenv("AIPROXY_TOKEN")
    if not api_key:
        return {"error": "Missing API key. Set AIPROXY_TOKEN in the environment."}

    client = OpenAI(api_key=api_key)

    prompt = f"""
    You are an intelligent task parser for an automation system. Given a task description in plain English, 
    extract the corresponding action and parameters.

    The task must be classified into one of the following actions:
    ["install_and_run", "format_markdown", "count_wednesdays", "sort_contacts", "extract_recent_logs",
    "extract_markdown_titles", "extract_email_sender", "extract_credit_card", "find_similar_comments", "calculate_sales"]

    Each action has specific required parameters:

    - "install_and_run":
      - "script_url" (str): The URL of the script to run.
      - "arg" (str): The argument to pass to the script.

    - "format_markdown":
      - "file" (str): Path to the Markdown file.
      - "prettier_version" (str): The version of Prettier to use.

    - "count_wednesdays":
      - "input_file" (str): Path to the file containing dates.
      - "output_file" (str): Path where the count should be saved.

    - "sort_contacts":
      - "input_file" (str): Path to the contacts JSON file.
      - "output_file" (str): Path where the sorted JSON should be saved.

    - "extract_recent_logs":
      - "log_dir" (str): Directory containing log files.
      - "output_file" (str): Path where extracted lines should be saved.
      - "count" (int): Number of log files to process.

    - "extract_markdown_titles":
      - "docs_dir" (str): Directory containing Markdown files.
      - "output_file" (str): Path where the extracted titles should be saved.

    - "extract_email_sender":
      - "input_file" (str): Path to the email file.
      - "output_file" (str): Path where extracted email should be saved.

    - "extract_credit_card":
      - "input_file" (str): Path to the image file.
      - "output_file" (str): Path where extracted card number should be saved.

    - "find_similar_comments":
      - "input_file" (str): Path to the file containing comments.
      - "output_file" (str): Path where the most similar comments should be saved.

    - "calculate_sales":
      - "db_file" (str): Path to the SQLite database.
      - "ticket_type" (str): The type of ticket to filter.
      - "output_file" (str): Path where the total sales should be saved.

    Extract the relevant details from the following task description:

    Task: "{task}"

    Respond strictly in JSON format.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a precise and structured task parser.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        # Corrected response parsing
        result_content = response.choices[0].message.content.strip()

        # Ensure the response is valid JSON
        parsed_result = json.loads(result_content)
        return parsed_result

    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON response from OpenAI."}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


if __name__ == "__main__":
    task_description = "The file /data/dates.txt contains a list of dates, one per line. Count the number of Wednesdays in the list, and write just the number to /data/dates-wednesdays.txt"
    result = parse_task_with_llm(task_description)
    print(json.dumps(result, indent=4))
