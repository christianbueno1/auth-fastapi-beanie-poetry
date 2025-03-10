# Use the official Python 3.13 slim image
FROM docker.io/python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1     PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     && rm -rf /var/lib/apt/lists/*

# Copy the project files
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry==1.8.3

# Copy Poetry configuration files
# COPY pyproject.toml poetry.lock* README.md ./
COPY pyproject.toml poetry.lock* ./

# Configure Poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install Python dependencies
# use --no-root to skip installing the package itself
# --no-dev is deprecated and will be removed in future versions
# use --only main to install only the main dependencies
RUN poetry install --no-root --no-interaction --no-ansi --only main
# RUN poetry install --no-interaction --no-ansi --no-dev && poetry install --only-root
# RUN poetry install --no-interaction --no-ansi --only main

# Copy application code
COPY . .


# Expose the FastAPI port
EXPOSE 8000

# Run the FastAPI application
CMD ["poetry", "run", "uvicorn", "auth_fastapi_beanie_poetry.main:app", "--host", "0.0.0.0", "--port", "8000"]
