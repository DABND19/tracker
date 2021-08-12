FROM python:3

WORKDIR /tracker

COPY requirements.txt requirements.txt
RUN pip3 install -U -r requirements.txt
