FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y netcat-openbsd \
    && pip install --no-cache-dir -r requirements.txt

CMD ["sh", "./wait-for-mysql.sh"]
