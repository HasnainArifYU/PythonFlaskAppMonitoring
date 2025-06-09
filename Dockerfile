FROM python:3.11-slim

WORKDIR /app

RUN pip install flask prometheus_client

COPY . /app

EXPOSE 5000

CMD ["python", "app.py"]

