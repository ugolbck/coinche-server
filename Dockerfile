# Build stage
FROM ghcr.io/astral-sh/uv:latest-python3.12-slim as builder

WORKDIR /app

# Copy only the files needed for dependency installation
COPY pyproject.toml uv.lock ./

# Set UV optimization flags
ENV UV_SYSTEM_PYTHON=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_CACHE=1
ENV UV_LINK_MODE=copy

# Install dependencies in non-editable mode
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-editable

# Copy the rest of the application code
COPY . .

# Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-editable

# Production stage
FROM python:3.12-slim

WORKDIR /app

# Install only the required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the installed virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy only the necessary application files
COPY --from=builder /app/app ./app
COPY --from=builder /app/alembic.ini ./
COPY --from=builder /app/migrations ./migrations

# Set environment path to use the virtual environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app:$PATH"

# Create a non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# The command is set in compose.yml/compose.prod.yml
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
