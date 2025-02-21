# LLM-based Automation Agent

## Overview
This project is an automation agent that executes plain-English tasks by leveraging a Large Language Model (LLM). The agent processes log files, reports, and other structured/unstructured data to automate routine tasks within the Continuous Integration (CI) pipeline of DataWorks Solutions. The agent exposes an API that enables users to run specific tasks and retrieve output files.

## Features
- Supports multiple deterministic and non-deterministic automation tasks.
- Integrates an LLM (GPT-4o-Mini) for task interpretation and execution.
- Provides API endpoints to execute tasks and read output files.
- Ensures security by restricting data access to the `/data` directory and preventing file deletion.
- Packaged as a Docker image for easy deployment.

## API Endpoints
### 1. Execute Task
**Endpoint:** `POST /run?task=<task description>`  
**Description:** Executes a plain-English task by parsing and performing the required steps.

- **Success (200 OK)**: Task executed successfully.
- **Client Error (400 Bad Request)**: Invalid task description.
- **Server Error (500 Internal Server Error)**: Internal error in execution.

### 2. Read File Content
**Endpoint:** `GET /read?path=<file path>`  
**Description:** Retrieves the content of the specified file.

- **Success (200 OK)**: Returns the file content.
- **Not Found (404 Not Found)**: File does not exist.

## Tasks Implemented

### Phase A: Operations Tasks
- **A1**: Install `uv` (if required) and run `datagen.py` with `user.email` as an argument.
- **A2**: Format `/data/format.md` using `prettier@3.4.2`.
- **A3**: Count the number of Wednesdays in `/data/dates.txt` and write to `/data/dates-wednesdays.txt`.
- **A4**: Sort contacts in `/data/contacts.json` by `last_name` and `first_name`.
- **A5**: Extract the first line from the 10 most recent `.log` files in `/data/logs/`.
- **A6**: Index Markdown files in `/data/docs/` by extracting H1 titles.
- **A7**: Extract sender’s email address from `/data/email.txt` using an LLM.
- **A8**: Extract credit card number from `/data/credit-card.png` using an LLM.
- **A9**: Find the most similar pair of comments in `/data/comments.txt` using embeddings.
- **A10**: Calculate total sales for "Gold" ticket type from `/data/ticket-sales.db`.

### Phase B: Business & Security Tasks
- **B1**: Restrict data access to `/data` directory.
- **B2**: Prevent file deletion.
- **B3**: Fetch data from an API and save it.
- **B4**: Clone a Git repository and make a commit.
- **B5**: Run SQL queries on SQLite/DuckDB.
- **B6**: Extract data from a website (web scraping).
- **B7**: Compress or resize an image.
- **B8**: Transcribe audio from an MP3 file.
- **B9**: Convert Markdown to HTML.
- **B10**: Write an API endpoint to filter a CSV file and return JSON data.

## Installation & Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/user-name/repo-name.git
   cd repo-name
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   python app.py
   ```
4. Set the environment variable for AI Proxy:
   ```sh
   export AIPROXY_TOKEN=your-token-here
   ```
5. Run the application with Docker:
   ```sh
   docker run --rm -e AIPROXY_TOKEN=$AIPROXY_TOKEN -p 8000:8000 user-name/repo-name
   ```

## Deployment
1. Build the Docker image:
   ```sh
   docker build -t user-name/repo-name .
   ```
2. Push to Docker Hub:
   ```sh
   docker tag user-name/repo-name user-name/repo-name:latest
   docker push user-name/repo-name:latest
   ```
3. Run the container:
   ```sh
   podman run --rm -e AIPROXY_TOKEN=$AIPROXY_TOKEN -p 8000:8000 user-name/repo-name
   ```

## Submission
1. Ensure your GitHub repository is public and contains:
   - Source code
   - MIT LICENSE file
   - Dockerfile
2. Submit the following details via the provided Google Form:
   - **GitHub Repo URL**: `https://github.com/user-name/repo-name`
   - **Docker Image Name**: `user-name/repo-name`

## Evaluation Criteria
- **Phase A (10 Marks)**: 1 mark per correctly handled operations task.
- **Phase B (10 Marks)**: 1 mark per correctly handled business/security task.
- **Bonus Marks**:
  - Additional unlisted tasks handled.
  - Unique code implementation.

## Notes
- Use the AI Proxy token with `GPT-4o-Mini`.
- Ensure each API call completes within 20 seconds.
- Keep prompts concise to optimize token usage.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

