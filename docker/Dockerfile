FROM python:3.7.1

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL=C.UTF-8
ENV TZ=Europe/Rome
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install some packages

RUN apt-get update && apt-get install -y \
    software-properties-common \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# compose all requirements and install
COPY *requirements.txt /

RUN for f in /*requirements.txt; do (cat "${f}"; echo) >> tmp.txt; done
RUN cat tmp.txt
RUN rm /*requirements.txt
RUN mv /tmp.txt /requirements.txt

RUN pip install -r /requirements.txt

WORKDIR /var/project