FROM python:3-slim
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc \
		libxml2-dev \
		libxslt-dev \
        libpng-dev \
        libjpeg-dev \
        libtiff-dev \
	&& rm -rf /var/lib/apt/lists/*
RUN mkdir /code
WORKDIR /code
RUN pip install pipenv
ADD Pipfile /code/
ADD Pipfile.lock /code/
RUN pipenv install
ADD payments-app /code/payments-app
WORKDIR /code/payments-app
RUN pipenv run "python manage.py migrate"
CMD pipenv run "gunicorn wsgi --bind 0.0.0.0:8000"