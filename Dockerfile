FROM python:3.11-slim

WORKDIR /app
COPY ai-review/ ai-review/
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "ai-review/reviewer.py"]