FROM python:3.10.5-slim-buster

ENV TZ=Europe/Moscow
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /app

RUN python -m pip install --upgrade pip setuptools

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .
EXPOSE 80

ENTRYPOINT ["python", "main.py"]