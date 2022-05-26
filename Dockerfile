FROM python:3.9.7-slim

WORKDIR /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app
ENV PYTHONPATH=/app
CMD ["python", "app/main.py"]
