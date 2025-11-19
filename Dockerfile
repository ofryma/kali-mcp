FROM kalilinux/kali-rolling:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    API_PORT=5000 \
    DEBUG_MODE=0

# Update and install essential packages
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    nmap \
    gobuster \
    dirb \
    nikto \
    sqlmap \
    hydra \
    john \
    wpscan \
    enum4linux \
    curl \
    wget \
    netcat-traditional \
    dnsutils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
# Using --break-system-packages is safe in Docker containers as they are isolated
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Copy application files
COPY kali_server.py .
COPY LICENSE .

# Make scripts executable
RUN chmod +x kali_server.py

# Expose the API port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import requests; requests.get('http://localhost:5001/health', timeout=5)" || exit 1

# Default command runs the kali_server
CMD ["python3", "kali_server.py", "--ip", "0.0.0.0", "--port", "5001"]

