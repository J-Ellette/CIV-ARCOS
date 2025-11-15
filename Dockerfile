# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY civ_arcos/ ./civ_arcos/

# Create data directory
RUN mkdir -p /data/evidence

# Set environment variables
ENV ARCOS_STORAGE_PATH=/data/evidence
ENV ARCOS_PORT=8000

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "civ_arcos.api"]
