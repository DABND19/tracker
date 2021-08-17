FROM python:3

WORKDIR /src

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -U -r requirements.txt
