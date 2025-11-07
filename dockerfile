FROM python:3.11-slim

# Configura encoding PARA RESOLVER O ERRO
ENV PYTHONUTF8=1
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    libaio1 \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements primeiro (para cache eficiente)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
COPY . .

CMD ["python", "src/api_railway.py"]