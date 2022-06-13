FROM python:3.8.3

#RUN apt-get update -y
#RUN apt-get upgrade -y

WORKDIR /app
COPY ./ ./

RUN pip install -r requirements.txt
RUN python manage.py collectstatic


