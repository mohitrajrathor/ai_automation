FROM python:3

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . /app

# Create a virtual environment
RUN pip install -r requirements.txt

# Expose the FastAPI default port
EXPOSE 8000

# Command to run FastAPI using Uvicorn
# CMD ["venv/bin/python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
