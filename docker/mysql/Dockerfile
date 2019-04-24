FROM ubuntu:18.10
LABEL version="1.0"

# Prepare environment
ENV DEBIAN_FRONTEND noninteractive



# Install.
RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y install gnupg2  && \
  apt-get -y upgrade && \
  apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8507EFA5 && \
  apt-get update && \
  apt-get install -y build-essential && \
  apt-get install -y software-properties-common  wget && \
  wget https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb && \
  dpkg -i percona-release_latest.$(lsb_release -sc)_all.deb && \
  apt-get update && \
  apt-get install -y percona-server-server-5.7 percona-server-client-5.7 && \
  apt-get install -y locales git htop vim mc net-tools && \
  apt-get clean && \
  rm -rf /tmp/* /var/lib/apt/lists/* /var/tmp/*;

# fix locales
ADD config/locales /var/lib/locales/supported.d/local
RUN locale-gen

ADD config/my.cnf /etc/mysql/my.cnf
RUN chmod 755 /etc/mysql/my.cnf
#RUN addgroup --gid 950 mysql || true
#RUN adduser --quiet --system --disabled-login --no-create-home --uid 950 --gid 950  mysql || true
RUN mkdir -p /home/mysql
RUN mysqld --initialize-insecure --datadir=/home/mysql/
# mysql -uroot -p

# install minit
RUN mkdir -p /etc/minit
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E007F6BD
RUN echo "deb http://ppa.launchpad.net/chazomaticus/minit/ubuntu xenial main" > /etc/apt/sources.list.d/minit.list
RUN apt-get update && apt-get upgrade -y && apt-get install -y minit
RUN apt-get clean
RUN rm -rf /tmp/* /var/lib/apt/lists/* /var/tmp/*



ADD create_base.sh /root/create_base.sh
RUN chmod 755 /root/create_base.sh

ADD startup.sh /etc/minit/startup
RUN chmod 755 /etc/minit/startup

EXPOSE 3306

CMD ["/sbin/minit"]
# EOF

#docker build -t mysqltest .
#docker run -d -it -p 0.0.0.0:3311:3306 --name=kz mysqltest
#docker exec -it kz bash
#
#DELETE
#docker stop kz
#docker rm kz
#docker rmi mysqltest





