# Build stage
FROM python:3.10-slim AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.10-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application code
COPY . .

# # Create data directory if it doesn't exist
# RUN mkdir -p data

# # Set up database if it doesn't exist and wait for completion
# RUN if [ ! -f data/red_team_prompt_database.db ]; then \
#         echo "Setting up red team prompt database..." && \
#         cd scripts && \
#         python3 generate_red_team_prompts.py && \
#         cd .. && \
#         while [ ! -f data/red_team_prompt_database.db ] || [ ! -s data/red_team_prompt_database.db ]; do \
#             echo "Waiting for database to be generated..." && \
#             sleep 5; \
#         done && \
#         echo "Database generation completed."; \
#     else \
#         echo "Database already exists, skipping setup."; \
#     fi

# Set ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Remember the problems getting NLTK to work in docker:
# # COPY download_nltk_models.py /app/