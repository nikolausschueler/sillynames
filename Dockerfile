FROM ubuntu:latest

RUN apt-get update

RUN apt-get install -y python
RUN apt-get install -y python-pip

# Install Flask via pip because the version installed by apt-get does not have
# the flask command line tool.
RUN pip install flask
RUN pip install flask-wtf

COPY ./names.csv /
COPY ./names.py /
COPY ./static /static
COPY ./templates /templates
COPY ./run-on-docker.sh /
COPY ./seleniumtest.py /

#ENTRYPOINT /./run-on-docker.sh
CMD /./run-on-docker.sh
