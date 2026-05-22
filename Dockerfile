FROM ghcr.io/astral-sh/uv:alpine3.23

WORKDIR /app

RUN apk add ffmpeg gcc musl-dev python3-dev alsa-lib-dev pkgconf
ADD pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

CMD ["uv", "run", "python", "-m", "app"]