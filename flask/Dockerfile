FROM python:3.7-buster

RUN pip install --upgrade pip && \
    pip install pipenv  


WORKDIR /app

COPY . /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pipenv install --system 

CMD [ "uwsgi", "app.ini" ]
