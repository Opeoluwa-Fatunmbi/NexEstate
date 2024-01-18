FROM python:3.11-slim-buster

RUN apt-get update

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV APP_HOME=/build
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles

LABEL maintainer='opeoluwafatunmbi@gmail.com'
LABEL description="Development image for NexEstate API"

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

# We create folder named build for our app.
WORKDIR $APP_HOME

COPY ./initials ./initials
COPY ./.env .
COPY ./requirements.txt .

# We copy our app folder to the /build

RUN pip install -r requirements.txt

COPY ./initials/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./initials/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

ENTRYPOINT [ "/entrypoint" ]