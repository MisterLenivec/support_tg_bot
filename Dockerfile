FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip3 install --upgrade setuptools
RUN pip3 install -r /app/requirements.txt

RUN chmod 755 .
COPY . /app
