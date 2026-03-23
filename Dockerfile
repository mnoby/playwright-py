# ── Stage 1: base image with system deps ──────────────────────────────────
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy AS base

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (already included in base image, but explicit)
RUN playwright install chromium --with-deps

# ── Stage 2: final image ───────────────────────────────────────────────────
FROM base AS final

WORKDIR /app

# Copy project
COPY . .

# Create directories for reports/artifacts
RUN mkdir -p reports/screenshots reports/videos

# Default env is dev; override at runtime with --env or ENV variable
ENV ENV=dev
ENV HEADLESS=true

# Entrypoint: run pytest and pass through any extra args
ENTRYPOINT ["pytest"]
CMD ["--env", "dev"]