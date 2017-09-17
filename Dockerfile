FROM ubuntu:17.04

USER root
RUN apt-get update && \
    apt-get install python3.6 python3-pip git unzip -y

RUN useradd -ms /bin/bash telegram

WORKDIR /home/telegram

USER telegram

COPY deploy.zip deploy.zip
RUN unzip deploy.zip

USER root
RUN pip3 install -r requirements.txt

USER telegram

ARG telegram_token
ENV TELEGRAM_TOKEN $telegram_token

ARG subscription_key
ENV SUBSCRIPTION_KEY $subscription_key

CMD python3 main.py




