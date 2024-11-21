FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

RUN mkdir -p static/uploads && \
    chmod 777 static/uploads

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "4"] 