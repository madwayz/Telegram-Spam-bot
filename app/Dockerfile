FROM ubuntu:bionic

WORKDIR /app
ADD . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa

RUN apt-get install -y python3-dev zlib1g-dev python3.8 python3-pip netcat

RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install -r requirements.txt

ENTRYPOINT ["bash", "entrypoint.sh"]