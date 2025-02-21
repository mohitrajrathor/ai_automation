# Use a Python image that also supports Node.js if needed
FROM python:3

# Set the working directory
WORKDIR /app

# Copy and install dependencies first to optimize caching
COPY . /app

# Install dependencies in a virtual environment
RUN pip install -r requirements.txt

# Copy the rest of the project files

# Expose the FastAPI default port
EXPOSE 8000

# Command to run FastAPI using Uvicorn inside the virtual environment
CMD ["fastapi", "run", "main.py"]
