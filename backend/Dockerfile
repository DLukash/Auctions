FROM python:3.8.3 as base
WORKDIR /app

#RUN apt-get update -y
#RUN apt-get upgrade -y

# TODO add stage with volume


FROM base as dev
COPY ./requirements.txt ./
RUN pip install -r requirements.txt


FROM base as prod
COPY ./ ./
RUN pip install -r requirements.txt

# RUN python manage.py collectstatic --noinput


