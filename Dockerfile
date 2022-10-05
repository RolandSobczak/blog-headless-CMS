FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements/base.txt /code/
COPY requirements/develop.txt /code/
COPY requirements/production.txt /code/
RUN pip install -r base.txt
RUN apt update
COPY . /code/