from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load FLAN-T5 small model and tokenizer
model_name = "google/flan-t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)


def generate_response(task: str) -> str:
    # Generate a response using FLAN-T5

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

    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output_ids = model.generate(input_ids, max_length=1024, num_beams=4)
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response


if __name__ == "__main__":
    # Example usage
    prompt = "What is the capital of France?"
    response = generate_response(prompt)
    print(response)
