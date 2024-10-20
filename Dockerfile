FROM python:3.11-slim

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         nginx \
         ffmpeg \
         libsm6 \
         libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY deepface-sagemaker/ /opt/program

WORKDIR /opt/program

RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

RUN chmod +x /opt/program/serve