FROM python:alpine

# Evitá errores por falta de compiladores
RUN apk add --no-cache gcc musl-dev

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["python", "app.py"]
