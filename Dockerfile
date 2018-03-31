FROM ubuntu:latest

RUN apt-get update

RUN apt-get install -y python3
RUN apt-get install -y python3-pip

# Install Flask via pip because the version installed by apt-get does not have
# the flask command line tool.
RUN pip3 install flask
RUN pip3 install flask-wtf

COPY ./names.csv /
COPY ./names.py /
COPY ./static /static
COPY ./templates /templates
COPY ./seleniumtest.py /

CMD /./names.py
