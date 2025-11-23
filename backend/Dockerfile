FROM python:3.11-slim

LABEL org.opencontainers.image.source="https://github.com/ansh-verma1404/k8s-yaml-analyzer"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Correct copy path
COPY k8s_analyzer /app/k8s_analyzer
COPY cli.py /app/cli.py

EXPOSE 8443
CMD ["uvicorn", "k8s_analyzer.main:app", "--host", "0.0.0.0", "--port", "8443"]
