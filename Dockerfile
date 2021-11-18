FROM python:3.8-slim-buster
COPY hallo-world.py run.py
RUN run.py