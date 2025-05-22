FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock .python-version ./

RUN uv sync --no-dev

COPY . .

CMD ["sh", "-c", "uv run alembic upgrade head && uv run python -m src.main"]