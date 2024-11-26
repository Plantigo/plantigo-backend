FROM python:3.12-slim

WORKDIR /code

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/code:$PYTHONPATH"

COPY ./devices/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./devices /code/
COPY ./shared /code/shared
COPY ./scripts/generate_proto_files.sh /code/generate_proto_files.sh

RUN chmod +x /code/generate_proto_files.sh

EXPOSE 50051

ENTRYPOINT ["/bin/sh", "/code/generate_proto_files.sh"]
CMD ["python", "grpc_runner.py"]
