FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder
WORKDIR /app
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev
# COPY . .

FROM gcr.io/distroless/python3-debian12
WORKDIR /app
COPY /src src
COPY --from=builder /app/.venv /app/.venv
# COPY --from=builder /app .
ENV PATH="/app/.venv/bin:$PATH"
CMD ["main.py"]