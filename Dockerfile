FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY rag ./rag
COPY scripts ./scripts
COPY index ./index
COPY knowledge_base ./knowledge_base

CMD ["python", "-m", "rag.bot"]
