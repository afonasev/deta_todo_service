# For more information
# https://testdriven.io/blog/docker-best-practices/
# Builder image
FROM python:3.10-slim as builder

WORKDIR /tmp

# Install system deps
RUN apt-get update && \
    apt-get install gcc -y && \
    apt-get clean && \
    pip install --upgrade pip poetry

# Install python deps
COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry config virtualenvs.create false && \
    poetry export --without-hashes --dev | \
    pip install --ignore-installed --prefix=/deps -r /dev/stdin

# Runtime image
FROM python:3.10-slim as dev

WORKDIR /app

# Common python envs
ENV PYTHONDONTWRITEBYTECODE=true
ENV PYTHONFAULTHANDLER=true
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=true

# Install system deps
RUN apt-get update && \
    apt-get install make -y && \
    apt-get clean

# Use non-root user
RUN addgroup --gid 1001 --system app && \
    adduser \
    --no-create-home \
    --shell /bin/false \
    --disabled-password \
    --uid 1001 \
    --system \
    --group app
USER app

# Copy application deps
COPY --from=builder /deps /usr/local

# Copy application source code
COPY ./app /app/app

EXPOSE 8080
