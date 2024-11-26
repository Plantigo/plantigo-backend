FROM python:3.12-slim

WORKDIR /code

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH="/code:$PYTHONPATH" \
    DJANGO_SETTINGS_MODULE=core.settings

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY ./gateway/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./gateway /code/
COPY ./shared /code/shared
COPY ./scripts/generate_proto_files.sh /code/generate_proto_files.sh
COPY ./gateway/entrypoint.sh /code/entrypoint.sh

RUN chmod +x /code/generate_proto_files.sh /code/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/code/entrypoint.sh"]
