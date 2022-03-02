FROM python:3.10.2

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
CMD ["gunicorn", "--bind=0.0.0.0:5000", "wsgi:app"]