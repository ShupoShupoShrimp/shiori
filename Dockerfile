# ========= GLOBAL VARIABLE =========
ARG PYTHON=python:3.12-slim-bookworm@sha256:935c3c5b12357a7e10caa9c1e6ca5692344d97cf229832ef584be2cec9fc03df

# ========= BUILDER PHASE =========
FROM ${PYTHON} AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

COPY pyproject.toml uv.lock README.md* ./

RUN uv sync --frozen --no-cache --no-install-project

COPY src/ ./src/

RUN uv sync --frozen --no-cache


# ========= BUILDER PHASE =========
FROM ${PYTHON} AS final

WORKDIR /app

ARG UID=10001
ARG GID=10001

RUN groupadd -g ${GID} -r sea_group && \
useradd -u ${UID} -g sea_group -r -s /sbin/nologin sea_user

COPY --from=builder /app/.venv /app/.venv
COPY src/ ./src/

RUN chown -R ${UID}:${GID} /app

ENV PATH="/app/.venv/bin:$PATH"

USER ${UID}

CMD ["uvicorn", "shiori.api.main:app", "--reload", "--host", "0.0.0.0" ,"--port", "8000"]