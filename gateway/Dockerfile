FROM python:3.12-slim

WORKDIR /code

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH="/code:$PYTHONPATH" \
    DJANGO_SETTINGS_MODULE=core.settings \
    DEBIAN_FRONTEND=noninteractive

# Instalacja niezbędnych pakietów systemowych
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    postgresql-client \
    netcat-traditional \
    curl \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Instalacja zależności Pythona
COPY ./gateway/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie kodu aplikacji
COPY ./gateway /code/
COPY ./gateway/entrypoint.sh /code/entrypoint.sh

# Popraw line endings i ustaw uprawnienia
RUN dos2unix /code/entrypoint.sh && \
    chmod +x /code/entrypoint.sh && \
    chown root:root /code/entrypoint.sh

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

ENTRYPOINT bash /code/entrypoint.sh
