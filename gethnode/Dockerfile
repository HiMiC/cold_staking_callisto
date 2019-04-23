FROM ubuntu:18.10
LABEL version="1.0"

MAINTAINER Babichev Igor <himic5@yandex.ru>

# Prepare environment
ENV DEBIAN_FRONTEND noninteractive
ENV SHELL /bin/bash
ENV ENV="/etc/profile"

#ENTRYPOINT ['/bin/bash']

RUN rm /bin/sh && ln -s /bin/bash /bin/sh && \
  apt-get update && \
  apt-get -y upgrade

RUN \
  apt-get install -y build-essential && \
  apt-get install -y software-properties-common && \
  apt-get install -y locales ca-certificates git htop vim wget mc net-tools make gcc musl-dev && \
  apt-get clean && \
  rm -rf /tmp/* /var/lib/apt/lists/* /var/tmp/*;

RUN \
 cd /tmp && \
 wget https://dl.google.com/go/go1.11.linux-amd64.tar.gz && \
 tar -xvf go1.11.linux-amd64.tar.gz && \
 mv go /usr/local && \
 rm -rf /tmp/*

RUN  \
 echo "#!/bin/bash" >> /etc/profile.d/go.sh && \
 echo "" >> /etc/profile.d/go.sh && \
 echo "export GOROOT=/usr/local/go" >> /etc/profile.d/go.sh && \
 echo "export GOPATH=$HOME/go" >> /etc/profile.d/go.sh && \
 export GOROOT=/usr/local/go && \
 export GOPATH=$HOME/go && \
 echo "export PATH=$GOPATH/bin:$GOROOT/bin:$PATH" >> /etc/profile.d/go.sh && \
 chmod +x /etc/profile.d/go.sh && \
 export PATH=$GOPATH/bin:$GOROOT/bin:$PATH && \
 . /etc/profile.d/go.sh && \
 cd /opt/ && \
 git clone https://github.com/EthereumCommonwealth/go-callisto.git --depth 1

RUN . /etc/profile.d/go.sh && \
 cd /opt/go-callisto && \
 go version && \
 make geth && \
 cp /opt/go-callisto/build/bin/geth /usr/local/bin/geth

EXPOSE 8545 8546 30303 30303/udp








