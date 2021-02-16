FROM python:3.6.8-alpine3.9

ENV GROUP_ID=1000 \
    USER_ID=1000

LABEL MAINTAINER="Dave Conroy <dconroy@gmail.com>"
LABEL MAINTAINER="Josh Darnell <josh@kurotek.com>"

WORKDIR /var/www
ADD . /var/www/

RUN apk --update add python py-pip

# Added for tests
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base 

RUN pip install --upgrade pip \
  && pip install --upgrade -r requirements-test.txt \
  && pip install gunicorn

# Added for tests
RUN  apk del build-dependencies

RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

USER www

EXPOSE 5000

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsgi", "-t 600"]
