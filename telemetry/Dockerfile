
FROM python:3.12-alpine


WORKDIR /code

ENV PYTHONUNBUFFERED=1
COPY ./requirements.txt /code/requirements.txt

RUN pip install uv && uv pip install --system --no-cache -r requirements.txt


COPY . /code/


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
