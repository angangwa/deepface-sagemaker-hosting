FROM python:3.11

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         python3 \
         nginx \
         ca-certificates \
         ffmpeg \
         libsm6 \
         libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY deepface-sagemaker/ /opt/program

RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py && \
    pip install -r /opt/program/requirements.txt && \
        rm -rf /root/.cache

# Set environment variables
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

WORKDIR /opt/program
RUN chmod +x /opt/program/serve