FROM python:3.12-slim

WORKDIR /code

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/code:$PYTHONPATH"

COPY ./telemetry/requirements.txt /code/requirements.txt

RUN pip install --no-cache -r requirements.txt

COPY ./telemetry /code/

COPY ./shared /code/shared

COPY ./scripts/generate_proto_files.sh /code/generate_proto_files.sh

RUN chmod +x /code/generate_proto_files.sh
ENTRYPOINT ["/bin/sh", "/code/generate_proto_files.sh"]

CMD ["python", "runner.py"]
