# Infrastructure decisions
## Base container image choice
To have a way to make the application portable and ready to integrate with CI/CD pipelines, we must choose a base image to make it ship with it. The basic principles this base image should follow are these:  

1. It should be **stable**, meaning that it should always work on a deterministic way to help avoiding with environment-dependant bugs and problems that could slow the development -or worse- crash a production release. To do that it should always ship with compatible and standard libraries and packages.
2. It should have **frequent updates**. This helps having a more reliable product, since if the libraries and packages it uses are as up-to-date as possible it will benefit from the bug fixes and the performance enhancements those updates usually mean soon.
4. It should ship with Python or allow installing Python in a fast way. Since the project works on top of Python, it is mandatory that the base image has a good compatibility with it and allows for fast Python workflows.
5. It should be as lightweight as possible without compromising the rest of the principles.

### Candidates
The different choices we considered are `python:3.9-slim` and `python:3.9-alpine`, maintained by the Docker community and `ubuntu:20.04`, maintained by Canonical and Tianon. We think about them to compare the image size, build speed and the overall performance.

The first question that araises is why did we choose Python version 3.9 with the first two containers. That's because the project uses type hinting generics in standard collections, which is a feature accepted in [PEP 585](https://www.python.org/dev/peps/pep-0585/) and added in Python 3.9, so that means that this application should test in this stage at least the minimum supported Python version.

### Tests made
We created three candidate Dockerfiles to carry out the tests. Take into account that the Dockerfiles are first drafts that written to ensure that the basic features requested were met, and the Dockerfile finally added to the repository won't necessarily be one of these.

<details><summary>Ubuntu Dockerfile</summary>

	FROM ubuntu:20.04

	LABEL maintainer="noise-kngdm <nyrsleep@protonmail.com>" version="1.0.0" 

	ENV DEBIAN_FRONTEND=noninteractive
	RUN groupadd -g 1000 -r music_matcher && useradd -u 1000 -r -g music_matcher music_matcher && \
		apt update && apt install -y python3.9 python3-pip curl python3.9-venv  && \
		mkdir -p /home/music_matcher/.local /app && chown -R music_matcher:music_matcher /home/music_matcher /app && \
		ln -sf /usr/bin/python3.9 /usr/bin/python3

	USER music_matcher

	COPY pyproject.toml poetry.lock tasks.py /app/

	WORKDIR /app/

	ENV PATH=$PATH:/home/music_matcher/.local/bin

	RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 - && \
		poetry config virtualenvs.create false && \
		poetry install

	ENTRYPOINT ["inv", "test"]

</details>

<details><summary>Python-alpine Dockerfile</summary>

	FROM python:3.9-alpine

	LABEL maintainer="noise-kngdm <nyrsleep@protonmail.com>" version="1.0.0" 

	RUN apk update && apk add curl gcc libc-dev libffi-dev bash && \
		addgroup -S -g 1000 music_matcher && \
		adduser -S music_matcher -G music_matcher -u 1000 && \
		mkdir -p /home/music_matcher/.local /app && \
		chown -R music_matcher:music_matcher /home/music_matcher /app

	USER music_matcher

	COPY pyproject.toml poetry.lock tasks.py /app/

	WORKDIR /app/

	ENV PATH=$PATH:/home/music_matcher/.local/bin

	RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python - && \
		poetry config virtualenvs.create false && \
		poetry install

	ENTRYPOINT ["inv", "test"]

</details>

<details><summary>Python-slim Dockerfile</summary>

	FROM python:3.9-slim

	LABEL maintainer="noise-kngdm <nyrsleep@protonmail.com>" version="1.0.0" 

	RUN groupadd -g 1000 -r music_matcher && useradd -u 1000 -r -g music_matcher music_matcher && \
		mkdir -p /home/music_matcher/.local /app && chown -R music_matcher:music_matcher /home/music_matcher /app && \
		apt update && apt install -y curl


	USER music_matcher

	COPY pyproject.toml poetry.lock tasks.py /app/

	WORKDIR /app/

	ENV PATH=$PATH:/home/music_matcher/.local/bin

	RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 - && \
		poetry config virtualenvs.create false && \
		poetry install

	ENTRYPOINT ["inv", "test"]
</details>

### Build times
We compared the build time of the three images using the `time` command. All the images required by each one of them were downloaded before the tests. The results obtained are the following:
```
docker build --no-cache . -f ./Dockerfile_py_slim -t py_slim_mm  0.04s user 0.05s system 0% cpu 36.564 total
docker build --no-cache . -f ./Dockerfile_py_alpine -t py_alpine_mm  0.04s user 0.05s system 0% cpu 57.674 total
docker build --no-cache . -f ./Dockerfile_ubuntu -t ubuntu_mm  0.09s user 0.12s system 0% cpu 53.406 total
```

It's clear that the `python/3.9-slim` had a smaller build time since it required less packages to be installed and could use the wheels provided by PyPI natively instead of having to compile them.

### Image size
As for the size of every builded image, a call to `docker images` returned this output.

```
ubuntu_mm                             latest            b820ce8dd31f   54 minutes ago      543MB
py_slim_mm                            latest            c92c62fcd0f2   56 minutes ago      222MB
py_alpine_mm                          latest            7a97c61cfd82   57 minutes ago      258MB
```

Again, the image based on `python:3.9-slim` have an advantage over the other two, although the difference with the one based on `python:3.9-alpine` is not decisive.

### Performance
While researching which would be the best image choice, we came around to articles like [this one](https://pythonspeed.com/articles/base-image-python-docker-images/), which state that it wouldn't be ideal to deploy Python applications using Alpine-based containers, since Alpine uses the `musl` implementation of the C standard library instead of the `glibc` one. This could be troublesome, because most of the Python wheels -precompiled and ready-to-use packages that are usually installed with pip- are compiled using `glibc`, and it hasn't been until recently that [PEP 656](https://www.python.org/dev/peps/pep-0656/) was approved. In this PEP, the PSF defines the `musllinux` tag to use when building Python wheels, which would end with the need of installing gcc and other GNU libraries in order to install some of our project's dependencies. Since this PEP was approved in 2021, not all libraries does ship that package yet -for example, [PyYaml](https://pypi.org/project/PyYAML/#files), one our project's dependencies doesn't-.

### Updates
As for the moment this document was written, Python versions `3.9.9` and even `3.10.1` were available for the `python:3.9-slim` and `python:3.9-alpine`, but the `ubuntu:20.04` image offered only Python up to version `3.9.5`.

### Final choice
It's clear that in almost all the checks performed the `python:3.9-slim` image was equal or better than the rest, so we decided using it as the base image of our Dockerfile. We'd reconsider changing it to `python:3.9-alpine` once the distribution of `musllinux` wheels is more extended in the Python community, since that would remove the necessity of installing `libc` and additional libraries in the alpine-based container to be able to install the project dependencies in a faster way.