FROM python:3

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY terenoi/requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/
