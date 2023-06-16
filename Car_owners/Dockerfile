# syntax=docker/dockerfile:1

FROM python:3.10.8-slim

ENV PYTHONUNBUFFERED=1

COPY . /Car_owners/

WORKDIR /Car_owners

RUN python -m venv /opt/venv
RUN pip install pip --upgrade
RUN pip install -r requirements.txt
