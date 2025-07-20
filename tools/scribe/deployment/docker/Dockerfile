# Scribe Engine v2.0 Production Dockerfile
# HMA v2.2 compliant containerized deployment

FROM python:3.12-slim as builder

# Set build arguments
ARG BUILD_VERSION=2.0.0
ARG BUILD_DATE
ARG VCS_REF

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create build directory
WORKDIR /build

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.12-slim as production

# Set metadata labels
LABEL maintainer="Scribe Engine Development Team" \
      version="${BUILD_VERSION}" \
      description="Scribe Engine v2.0 - HMA v2.2 compliant automation engine" \
      build.date="${BUILD_DATE}" \
      build.version="${BUILD_VERSION}" \
      build.vcs-ref="${VCS_REF}"

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r scribe && useradd -r -g scribe -d /app -s /bin/bash scribe

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/scribe/.local

# Copy application code
COPY --chown=scribe:scribe tools/scribe/ ./scribe/
COPY --chown=scribe:scribe tools/reports/ ./reports/

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/config /app/tmp && \
    chown -R scribe:scribe /app

# Copy configuration files
COPY --chown=scribe:scribe tools/scribe/config/ ./config/
COPY --chown=scribe:scribe tools/scribe/schemas/ ./schemas/

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    SCRIBE_CONFIG_PATH=/app/config/config.json \
    SCRIBE_LOG_LEVEL=INFO \
    SCRIBE_DATA_DIR=/app/data \
    SCRIBE_LOG_DIR=/app/logs \
    SCRIBE_TEMP_DIR=/app/tmp

# Switch to non-root user
USER scribe

# Add local bin to PATH
ENV PATH=/home/scribe/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:9469/health || exit 1

# Expose health check port
EXPOSE 9469

# Default command
CMD ["python", "-m", "scribe.engine", "--config", "/app/config/config.json"]