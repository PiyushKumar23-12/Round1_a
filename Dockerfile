FROM python:3.10-slim AS builder

WORKDIR /app

# Install system dependencies for PyMuPDF (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmupdf-dev gcc g++ && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip & install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install PyMuPDF==1.22.3 && \
    find /install -type d -name '__pycache__' -exec rm -rf {} + && \
    find /install -type f -name '*.pyc' -delete && \
    find /install -type d -name 'tests' -exec rm -rf {} +

# Stage 2: Minimal Runtime
FROM python:3.10-slim AS final

WORKDIR /app

# Copy only needed installed packages
COPY --from=builder /install /usr/local

# Copy your app
COPY app/main.py .

# Final command
CMD ["python", "main.py"]
