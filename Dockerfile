FROM python:3.12

COPY --from=ghcr.io/astral-sh/uv:0.13.5 /uv /uvx /bin/

WORKDIR /app

# イメージ内のPythonを使い、uv.lock どおりに本番用の依存のみインストールする
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-dev

COPY . .

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8080
ENV PYTHONUNBUFFERED True

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
