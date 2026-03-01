FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ADD pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
# RUN apt-get update  && \
#    uv run playwright install --with-deps firefox && \
#    rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["uv", "run", "python", "-m", "app"]