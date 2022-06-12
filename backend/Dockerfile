FROM python:3.8.3

#RUN apt-get update -y
#RUN apt-get upgrade -y

WORKDIR /app
COPY ./ ./

EXPOSE 8000-8000


ENTRYPOINT ["sh", "entrypoint.sh"]

#RUN pip install -r requirements.txt
#RUN python manage.py collectstatic

#CMD [ "gunicorn", "auction_backend.wsgi"]


