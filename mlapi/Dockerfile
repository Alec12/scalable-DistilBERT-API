# Stage 1 : Build venv as a temp environment
FROM python:3.11-slim AS venv

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
         curl \
         build-essential \
         libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry Globally
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set environment variables for Python and Poetry
ENV PATH="/root/.local/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create virtual environment outside of poetry
RUN python -m venv --copies /app/venv

# Cache dependencies
COPY pyproject.toml poetry.lock ./

# Activate venv and Install dependencies using poetry
RUN . /app/venv/bin/activate && poetry install --only main

# Build Runtime image
FROM python:3.11-slim AS prod

# Set working directory
WORKDIR /app

# Set env variables for Python Run
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/venv/bin:$PATH"

# Copy the venv from the builder stage
COPY --from=venv /app/venv /app/venv

# Copy the application code into the container
COPY . .

# Expose the application port for FastAPI
EXPOSE 8000

# Set up a health check for the container
HEALTHCHECK --start-period=30s CMD python -c "import requests; requests.get('http://localhost:8000/project/health', timeout=2)"

# Launch fastapi
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

