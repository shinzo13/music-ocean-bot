FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ADD pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
RUN apt-get update && \
    uv run playwright install-deps && \
    rm -rf /var/lib/apt/lists/*
RUN uv run playwright install firefox

COPY . .

#RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
#USER appuser

CMD ["uv", "run", "python", "-m", "app"]