# Use the official Python 3.13 slim image
FROM docker.io/python:3.13-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry==1.8.3

# Copy only dependency files first (better caching)
COPY pyproject.toml poetry.lock* ./

# Configure Poetry to avoid creating a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Define the command to run the FastAPI app
CMD ["uvicorn", "auth_fastapi_beanie_poetry.main:app", "--host", "0.0.0.0", "--port", "8000"]
