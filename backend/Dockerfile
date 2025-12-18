FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    libzbar0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 6543

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:6543/api/auth/me')" || exit 1

CMD ["python", "main.py"]
