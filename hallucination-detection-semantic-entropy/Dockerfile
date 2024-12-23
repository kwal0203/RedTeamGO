FROM python:3.12-slim-bullseye AS builder

# Install required system libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the environment file
RUN pip install -U pip

# # Activate the environment and install NLTK resources
COPY requirements.txt .
RUN pip install -r requirements.txt --force-reinstall

# Copy the script into the container
# COPY download_nltk_models.py /app/
COPY . .

# # Get service files
ADD service.py ./

# VERSION INFORMATION
ARG GIT_TAG ???
ARG GIT_COMMIT ???
ARG BUILD_DATE ???

ENV IVCAP_SERVICE_VERSION=$GIT_TAG
ENV IVCAP_SERVICE_COMMIT=$GIT_COMMIT
ENV IVCAP_SERVICE_BUILD=$BUILD_DATE

# Create necessary directories
RUN mkdir -p /data/in /data/out /cache

# Set the PYTHONPATH to include the src directory
ENV PYTHONPATH=/app/src

# Command to run
ENTRYPOINT ["python", "/app/service.py"]
