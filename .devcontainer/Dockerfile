FROM debian:bullseye-20250317-slim AS base

RUN apt-get update --fix-missing \
    && apt-get install -y sudo

RUN apt-get install -y \ 
    python3 \
    python3-pip

RUN sudo pip install pipenv

# RUN pipenv install django