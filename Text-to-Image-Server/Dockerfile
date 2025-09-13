FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV HUGGINGFACE_HUB_TOKEN=""

COPY . /app
WORKDIR /app
RUN uv sync --frozen --no-cache

CMD ["uv", "run", "run.py"]
