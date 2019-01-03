#docker build -t flag-gitbook .
#docker run -it --rm -v /home/oliver/Desktop/FlagDrillbook:/gitbook -p 4000:4000 flag-gitbook


FROM node

ARG VERSION=3.2.3

LABEL version=$VERSION

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y git

RUN npm install --global gitbook-cli \
        && gitbook fetch ${VERSION} \
        && npm cache verify \
        && rm -rf /tmp/*

WORKDIR /gitbook

RUN npm install --global gitbook-plugin-summary --save

VOLUME /gitbook

EXPOSE 4000 35729

CMD gitbook install && gitbook serve