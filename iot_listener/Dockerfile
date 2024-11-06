FROM python:3.9-slim
WORKDIR /app
COPY ../mqtt_listener_project/mqtt_listener .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
