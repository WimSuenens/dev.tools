# FROM debian:bullseye-20250317-slim AS base
# FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye
# FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm
# FROM debian:trixie-20250407
# FROM python:3.11.12-bookworm
# FROM python:3.11-alpine
# FROM mcr.microsoft.com/devcontainers/base:alpine
FROM mcr.microsoft.com/devcontainers/base:ubuntu

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

# RUN arch=$(arch | sed s/aarch64/arm64/ | sed s/x86_64/amd64/) && \
#     wget -O /tmp/wkhtmltox.deb "https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.bullseye_${arch}.deb"

# RUN apt-get update \
#     && apt-get install wget -y

# RUN arch=$(arch | sed s/aarch64/arm64/ | sed s/x86_64/amd64/) && \
#     wget -O /tmp/wkhtmltox.deb "https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.bookworm_${arch}.deb"

RUN arch=$(arch | sed s/aarch64/arm64/ | sed s/x86_64/amd64/) && \
    wget -O /tmp/wkhtmltox.deb "https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.jammy_${arch}.deb"

RUN apt-get update && sudo apt install -y -f /tmp/wkhtmltox.deb
# RUN apt-get update \ 
#     && apt-get install -y -f /tmp/wkhtmltox.deb

RUN apt-get update --fix-missing \ 
    && apt-get install -y build-essential \
    libpoppler-cpp-dev \
    ghostscript \
    ocrmypdf \
    poppler-utils

# RUN apk add ghostscript \
#     ocrmypdf \
#     poppler-utils

# https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user
# ARG USERNAME=vscode
# ARG USER_UID=1000
# ARG USER_GID=$USER_UID

# Create the user
# RUN addgroup -S $USERNAME \
#     && adduser -S $USERNAME -G $USERNAME
#     # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
#     # && apt-get update \
#     # && apt-get install -y sudo \
# RUN apk add sudo \
#     && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
#     && chmod 0440 /etc/sudoers.d/$USERNAME


# RUN apt-get install -y \
#     python3-pip \
#     pipx

# RUN pipx install pipenv
# RUN pipx ensurepath

# RUN arch=$(arch | sed s/aarch64/arm64/ | sed s/x86_64/amd64/) && \
#     sudo apt install -f /tmp/wkhtmltox_0.12.6.1-2.bullseye_${arch}.deb

# RUN apt-get install -y \ 
#     python3 \
#     python3-pip

# RUN sudo pip install pipenv

# RUN pipenv install django
# USER $USERNAME
# RUN echo "alias python=python3" >> ~/.bashrc

# RUN pipx install pipenv
# RUN pipx ensurepath
# RUN source ~/.bashrc
#  && pipenv install
# SHELL ["/bin/bash", "-l", "-c"]