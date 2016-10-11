FROM debian:jessie
MAINTAINER AJ Bowen <aj@soulshake.net>

RUN apt-get update && apt-get install -y \
    python-pip

COPY . /src/
WORKDIR /src/
RUN pip install .
ENTRYPOINT ["wakatime"]
