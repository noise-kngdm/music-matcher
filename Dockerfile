FROM python:3.9-slim

LABEL maintainer="noise-kngdm <nyrsleep@protonmail.com>" version="1.0.0" 

RUN groupadd -g 1000 -r music_matcher && \
    useradd -u 1000 -m -r -g music_matcher music_matcher

USER music_matcher

WORKDIR /app/test/

ENV PATH=$PATH:/home/music_matcher/.local/bin

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

ENTRYPOINT ["inv", "test"]
