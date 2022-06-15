FROM python:3.8.3 as base

#RUN apt-get update -y
#RUN apt-get upgrade -y

# TODO add stage with volume


FROM base as dev
WORKDIR /app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt


FROM base as prod
WORKDIR /app
COPY ./ ./
RUN pip install -r requirements.txt

# RUN python manage.py collectstatic --noinput


