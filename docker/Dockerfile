FROM python:3.7

RUN apt-get update
RUN apt-get install -y git
RUN git clone https://github.com/globz-eu/recipes-backend /usr/src/app
WORKDIR /usr/src/app
RUN pip3 install -r requirements.txt
RUN pip3 install uwsgi
CMD ["./run.sh"]
