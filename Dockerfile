FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y git && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["/usr/local/bin/python3", "main.py"]
