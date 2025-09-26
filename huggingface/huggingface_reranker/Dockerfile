FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV HF_HOME=/app/.cache

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY download_tokenizer.py .
RUN python download_tokenizer.py

CMD ["sleep", "infinity"]
