FROM python:3.10-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y git ffmpeg libgl1 wget && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy handler
COPY handler.py .

# Download model weights at build time (optional - or let it download on first run)
# RUN python -c "from transformers import AutoProcessor, AutoModelForVision2Seq; AutoProcessor.from_pretrained('Qwen/Qwen2.5-VL-3B-Instruct'); AutoModelForVision2Seq.from_pretrained('Qwen/Qwen2.5-VL-3B-Instruct')"

# Define handler entry point
CMD ["handler.handler"]
