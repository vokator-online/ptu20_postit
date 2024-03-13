# syntax=docker/dockerfile:1
FROM python:slim-bullseye
WORKDIR /app
COPY ./ptu20_postit .
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
# RUN python manage.py collectstatic --noinput
# RUN python manage.py migrate
# CMD ["gunicorn", "-b", "0.0.0.0:8000", "ptu20_postit.wsgi"]
