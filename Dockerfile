# ---- Base Image ----
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system-level dependencies (needed for some ML/data packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the master requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose the Streamlit default port
EXPOSE 8501

# Streamlit configuration: disable telemetry and run headlessly
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Health check to confirm the app is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Launch the Streamlit frontend
CMD ["streamlit", "run", "Phase_6_Web_UI/frontend/streamlit_app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0"]
