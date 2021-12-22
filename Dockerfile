FROM python:3.9-slim

LABEL maintainer="noise-kngdm <nyrsleep@protonmail.com>" version="1.0.0" 

RUN groupadd -g 1000 -r music_matcher && \
    useradd -u 1000 -m -r -g music_matcher music_matcher && \
    apt update && apt install -y curl

USER music_matcher

COPY pyproject.toml poetry.lock /music_matcher/

WORKDIR /music_matcher/test/

ENV PATH=$PATH:/home/music_matcher/.local/bin

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.create false && \
    poetry install

ENTRYPOINT ["inv", "test"]
