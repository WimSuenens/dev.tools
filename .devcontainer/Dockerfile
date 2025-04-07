# FROM debian:bullseye-20250317-slim AS base
FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

# RUN apt-get update --fix-missing \
#     && apt-get install -y sudo8

# RUN sudo apt-get update --fix-missing \
#     && sudo apt-get upgrade -y

# RUN sudo apt-get install -y \ 
#     fontconfig \
#     xfonts-75dpi \
#     xfonts-base

# https://stackoverflow.com/questions/70369368/check-architecture-in-dockerfile-to-get-amd-arm
# WORKDIR /tmp
RUN arch=$(arch | sed s/aarch64/arm64/ | sed s/x86_64/amd64/) && \
    wget -O /tmp/wkhtmltox.deb "https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.bullseye_${arch}.deb"

RUN sudo apt-get update && sudo apt install -y -f /tmp/wkhtmltox.deb

# RUN arch=$(arch | sed s/aarch64/arm64/ | sed s/x86_64/amd64/) && \
#     sudo apt install -f /tmp/wkhtmltox_0.12.6.1-2.bullseye_${arch}.deb

    # RUN apt-get install -y \ 
#     python3 \
#     python3-pip

# RUN sudo pip install pipenv

# RUN pipenv install django