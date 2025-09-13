FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV HUGGINGFACE_HUB_TOKEN=""

# Update package lists and install build essentials
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Set CC environment variable
ENV CC=gcc

COPY . /app
WORKDIR /app
RUN uv sync --frozen --no-cache

CMD ["uv", "run", "run.py"]
