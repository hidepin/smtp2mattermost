FROM python:alpine3.7

LABEL maintainer "Hidetoshi Imai <hidepin@gmail.com>"

ARG MATTERMOST_ADDRESS=127.0.0.1
ARG MATTERMOST_LOGIN_ID=admin
ARG MATTERMOST_PASSWORD=admin
ARG MATTERMOST_PORT=80
ENV MATTERMOST_ADDRESS=${MATTERMOST_ADDRESS} \
    MATTERMOST_LOGIN_ID=${MATTERMOST_LOGIN_ID} \
    MATTERMOST_PASSWORD=${MATTERMOST_PASSWORD} \
    MATTERMOST_PORT=${MATTERMOST_PORT}

RUN pip install mattermostdriver

COPY files/smtp2mattermost.py /usr/local/bin/smtp2mattermost.py

CMD ["/usr/local/bin/smtp2mattermost.py"]
