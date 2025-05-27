FROM python:3.11-slim

# Evitá errores por falta de compiladores
RUN apt-get update && apt-get install -y gcc build-essential

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["python", "app.py"]
