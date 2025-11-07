# 1. Use uma imagem base oficial do Python (leve)
FROM python:3.10-slim

# 2. Defina o diretório de trabalho *dentro* do container
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "api.py"]