FROM python:3.9-slim-buster

RUN apt-get clean && apt-get -y update
RUN apt-get -y install \
    apache2 \
    apache2-dev \
    fping

RUN pip install mod_wsgi
RUN mod_wsgi-express install-module >> /etc/apache2/apache2.conf
RUN echo 'ServerName localhost' >> /etc/apache2/apache2.conf
COPY wsgi.conf /etc/apache2/sites-enabled/000-default.conf

WORKDIR /pysmarthome

COPY requirements.txt pysmarthome-server.wsgi ./
RUN pip install -r requirements.txt

COPY pysmarthome_server ./pysmarthome_server

RUN chown www-data:www-data /usr/local/bin
RUN chown -R www-data:www-data /usr/local/lib/

CMD service apache2 restart && tail -f /var/log/apache2/*
