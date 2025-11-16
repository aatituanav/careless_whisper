FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    ffmpeg \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python3 -m pip install --no-cache-dir --upgrade pip

# Install Python dependencies
COPY builder/requirements.txt /app/builder/requirements.txt
RUN pip install --no-cache-dir -r /app/builder/requirements.txt

# Download models during build
COPY builder/download_models.py /app/builder/download_models.py
RUN python3 /app/builder/download_models.py

# Copy application code
COPY src/ /app/

# RunPod handler
CMD ["python3", "-u", "/app/rp_handler.py"]
