# syntax=docker/dockerfile:1
FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (tzdata for Europe/Berlin)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY infra/requirements.txt ./infra/requirements.txt
RUN pip install --no-cache-dir -r infra/requirements.txt

# App code
COPY agent ./agent
COPY .env.example ./

# Expose API
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "agent.api:app", "--host", "0.0.0.0", "--port", "8000"]
