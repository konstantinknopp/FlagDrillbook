#Step1: docker build -t flag-gitbook .
#Step2(automatisch) docker run -it --rm -p 4000:4000 flag-gitbook
#Step2(selbst rumspielen) :docker run -it --rm -v /home/oliver/Desktop/FlagDrillbook:/gitbook -p 4000:4000 flag-gitbook /bin/bash

FROM node

ARG VERSION=3.2.3

LABEL version=$VERSION

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y \
	git \
	calibre \
	nano

RUN npm install --global gitbook-cli \
        && gitbook fetch ${VERSION} \
        && npm cache verify \
        && rm -rf /tmp/*

RUN npm install --global gitbook-plugin-summary --save

WORKDIR /gitbook

VOLUME /gitbook

EXPOSE 4000 35729

CMD git clone https://github.com/obraunsdorf/FlagDrillbook/ \
	&& cd FlagDrillbook \
	&& gitbook install \
	&& gitbook build \
	&& gitbook serve
