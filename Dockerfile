FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git ffmpeg libgl1 wget && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY handler.py .

# 🟢 ENTRYPOINT استاندارد RunPod Serverless
CMD ["python3", "-m", "runpod"]
