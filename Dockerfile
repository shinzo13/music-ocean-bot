FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ADD pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
RUN apt-get update && \
    uv run playwright install-deps && \
    rm -rf /var/lib/apt/lists/*
RUN uv run playwright install firefox

COPY . .

CMD ["uv", "run", "python", "-m", "app"]