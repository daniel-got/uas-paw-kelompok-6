# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies (including libzbar for QRIS)
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libzbar0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 6543 (default Pyramid port)
EXPOSE 6543

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:6543/api/auth/me')" || exit 1

# Run the application
CMD ["python", "main.py"]
