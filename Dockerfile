# pull official base image
FROM python:3.10.7-slim-buster

# set work directory
WORKDIR /akindi-discord-mcq

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /akindi-discord-mcq/requirements.txt
RUN pip install -r /akindi-discord-mcq/requirements.txt

# copy project
COPY . /akindi-discord-mcq

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]
