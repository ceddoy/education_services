FROM python:3.8

ENV PYTHONUNBUFFERED 1
RUN mkdir /backend_service
WORKDIR /backend_service
COPY requirements.txt /backend_service/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /backend_service/
