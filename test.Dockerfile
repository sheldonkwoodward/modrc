FROM python:3.8-alpine
RUN mkdir -p /modrc/modrc
RUN mkdir -p /modrc/tests
WORKDIR /modrc
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
