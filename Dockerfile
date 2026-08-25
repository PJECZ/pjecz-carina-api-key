# Use an official Python runtime as a parent image
FROM python:3.14-slim

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install uv from official source
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory in the container
WORKDIR /app

# Set enviroment variables for uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

# Copy this for install dependencies with uv
COPY pyproject.toml uv.lock ./

# Install dependencies with uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy application code
COPY . .

# Install project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Expose port
EXPOSE 8000

# Command
CMD [ "gunicorn", "pjecz_casiopea_api_key.main:app", "--workers", "1", "--threads", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000" ]
