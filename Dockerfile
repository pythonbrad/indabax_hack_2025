FROM python:3.13-slim-bookworm AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Change the working directory to the `app` directory
WORKDIR /app

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates unzip

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-editable --no-dev --group prod

# Download geo data
RUN  --mount=type=cache,target=install-deps.sh \
     --mount=type=bind,source=install-deps.sh,target=install-deps.sh \
    ./install-deps.sh

# Copy the project into the intermediate image
ADD . /app

FROM python:3.13-slim-bookworm

WORKDIR /app

# Copy the environment, but not the source code
COPY --from=builder --chown=app:app /app /app

# Run the application
CMD [".venv/bin/python", "main.py"]
