FROM python:3.10-slim-bookworm

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /app

# Install minimal system dependencies only if needed
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip cleanly
RUN python -m pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir \
    pandas \
    sqlalchemy \
    psycopg2-binary \
    openpyxl \
    python-dotenv \
    psutil

COPY ingest_data.py .

ENTRYPOINT ["python", "ingest_data.py"]
