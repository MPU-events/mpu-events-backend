FROM python:3.13-slim

WORKDIR /app

#RUN apt-get update && apt-get install -y --no-install-recommends \
#    gcc \
#    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock* ./

RUN pip install uv && \
    uv pip install --system -e .

COPY src/ ./src/

RUN mkdir -p /app/config

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "mpu_events.main:app", "--host", "0.0.0.0", "--port", "8000"]