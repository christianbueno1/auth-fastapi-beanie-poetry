FROM docker.io/python:3.13-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry==1.8.3

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Configure Poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "auth_fastapi_beanie_poetry.main:app", "--host", "0.0.0.0", "--port", "8000"]