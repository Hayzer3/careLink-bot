FROM python:3.11-slim

WORKDIR /app

# Copia só requirements primeiro (cache eficiente)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia só o necessário
COPY src/ src/
COPY config/ config/
COPY bots/ bots/
COPY services/ services/
COPY utils/ utils/

CMD ["python", "src/api_railway.py"]