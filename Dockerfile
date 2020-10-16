FROM ubuntu:20.04

LABEL \
    name="PortalD" \
    author="Paulo Roberto Júnior <paulojrbeserra@gmail.com>" \
    maintainer="Paulo Roberto <paulojrbeserra@gmail.com>" \
    description="Portal-Dashboard"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y -qq && \
    apt-get install -y -qq --no-install-recommends \
        vim \
        curl \
        build-essential \
        libssl-dev \
        libffi-dev \
        locales \
        sudo \
        software-properties-common \
        python3.8 && \
    apt-get update -y -qq && \
    apt-get install -y -qq --no-install-recommends \
        libsasl2-dev \
        libldap2-dev \
        python3-pip \
        python3-dev \
        python3.8-venv \
        python3-virtualenv \
        libmysqlclient-dev \
        mysql-client

RUN ln /usr/bin/python3 /usr/bin/python

RUN apt-get install -y -qq \
    default-libmysqlclient-dev \
    apache2 \
    libapache2-mod-security2 \
    libapache2-mod-wsgi-py3

RUN a2enmod wsgi

RUN sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen

ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR:pt:en
ENV LC_ALL pt_BR.UTF-8

RUN apt remove -y && apt clean apt autoclean apt autoremove -y
RUN mkdir /var/www/portald/
WORKDIR /var/www/portald
COPY ./portald/ /var/www/portald/
## COPY ./config/000-default.conf /etc/apache2/sites-available

COPY ./wait-for-mysql.sh /

RUN sed -i -e 's/\r$//' /wait-for-mysql.sh
RUN chmod u+x /wait-for-mysql.sh

## COPY ./requirements.txt /code/
RUN python3 -m pip install --quiet --no-cache-dir -r /var/www/portald/requirements.txt

EXPOSE 8100
EXPOSE 9100
