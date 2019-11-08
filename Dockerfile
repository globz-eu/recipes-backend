FROM python:3.8

RUN apt-get update
RUN apt-get install -y git
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip3 install -r requirements.txt
RUN pip3 install uwsgi
ENTRYPOINT ["./run.sh"]
