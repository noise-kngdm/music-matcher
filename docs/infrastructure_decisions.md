# Infrastructure decisions
## Test container
### Base container image choice
To have a way to make the application portable and ready to integrate with CI/CD pipelines, we must choose a base image to make it ship with it. The basic principles this base image should follow are these:  

1. It should be **stable**, meaning that it should always work in a deterministic way to help to avoid environment-dependant bugs and problems that could slow the development -or worse- crash a production release. To do that it should always ship with compatible and standard libraries and packages.
2. It should have **frequent updates**. This helps to have a more reliable product since if the libraries and packages it uses are as up-to-date as possible it will benefit from the bug fixes and the performance enhancements those updates usually mean soon.
4. It should ship with Python or allow installing Python in a fast way. Since the project works on top of Python, it is mandatory that the base image has good compatibility with it and allows for fast Python workflows.
5. It should be as lightweight as possible without compromising the rest of the principles.

#### Candidates
The different choices we considered are [python:3.9-slim](https://github.com/docker-library/python/blob/3d43bcf8ddd26ae85fd6a63a7e1d502b445c9cce/3.9/bullseye/slim/Dockerfile) and [python:3.9-alpine](https://github.com/docker-library/python/blob/b739aec8401a072f43ed5f5eec806e8cc1d1b106/3.9/alpine3.15/Dockerfile), maintained by the Docker community and part of the [official Python image](https://hub.docker.com/_/python), and [ubuntu:20.04](https://github.com/tianon/docker-brew-ubuntu-core/blob/bf61e139e84e04f9d87fff5dc588a3f0398da627/focal/Dockerfile), maintained by Canonical and Tianon and part of the [official Ubuntu image] (https://hub.docker.com/_/ubuntu).

#### Why choosing those candidates
The reasons we thought of when choosing every candidate base image for the tests are the following:  

- **python:3.9-slim [Debian 11]**: we chose this version of Debian because it's the latest Debian's stable release and the one [recommended by its documentation](https://www.debian.org/releases/).
We think about them to compare the image size, build speed, and overall performance.  

- **python:3.9-alpine [Alpine 3.15]**: It's a fast and lightweight image, and one of the most popular base images for Docker containers. We chose the `3.15` version because it's the latest stable release of Alpine Linux.  

- **ubuntu:20.04 [Ubuntu 20.04]**: We thought about including one general-purpose OS with several tools in our tests -even though we knew we wouldn't end up choosing it from beforehand- to reassure the reasons why it would be more convenient to use a more lightweight image. We chose the `20.04` version because is the latest LTS Ubuntu version.  

#### Why Python 3.9
The first question that arises is why did we choose Python version 3.9 with the first two containers. That's because the project uses type hinting generics in standard collections, which is a feature accepted in [PEP 585](https://www.python.org/dev/peps/pep-0585/) and added in Python 3.9, so that means that this application should test in this stage at least the minimum supported Python version.

#### Tests performed
We created three candidate Dockerfiles to carry out the tests. Take into account that the Dockerfiles are first drafts that were written to ensure that the basic features requested were met, and the Dockerfile finally added to the repository won't necessarily be one of these.

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

	WORKDIR /app/test

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

	WORKDIR /app/test

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

	WORKDIR /app/test

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

It's clear that the `python/3.9-slim` had a smaller build time since it required fewer packages to be installed and could use the wheels provided by PyPI natively instead of having to compile them.

#### Image size
As for the size of every built image, a call to `docker images` returned this output.

```
ubuntu_mm                             latest            b820ce8dd31f   54 minutes ago      543MB
py_slim_mm                            latest            c92c62fcd0f2   56 minutes ago      222MB
py_alpine_mm                          latest            7a97c61cfd82   57 minutes ago      258MB
```

Again, the image based on `python:3.9-slim` has an advantage over the other two, although the difference with the one based on `python:3.9-alpine` is not decisive.

#### Performance
While researching which would be the best image choice, we came around to articles like [this one](https://pythonspeed.com/articles/base-image-python-docker-images/), which state that it wouldn't be ideal to deploy Python applications using Alpine-based containers, since Alpine uses the `musl` implementation of the C standard library instead of the `glibc` one. This could be troublesome, because most of the Python wheels -precompiled and ready-to-use packages that are usually installed with pip- are compiled using `glibc`, and it hasn't been until recently that [PEP 656](https://www.python.org/dev/peps/pep-0656/) was approved. In this PEP, the PSF defines the `musllinux` tag to use when building Python wheels, which would end with the need of installing gcc and other GNU libraries in order to install some of our project's dependencies in an Alpine-based container. Since this PEP was approved in 2021, not all libraries do ship that package yet -for example, [PyYaml](https://pypi.org/project/PyYAML/#files), one of our project's dependencies doesn't-. The inconvenience of having to install `glibc` and other libraries to compile some of the dependencies in the Alpine-based container affects both the image size and the build time.  

To compare how the different images perform we wrote a little script to calculate the mean time every image would take to execute the unit tests from a sample of 50 executions.

<details><summary>Python script</summary>

	import docker
	import os
	import re

	client = docker.from_env()
	regex_seconds = re.compile(r'\d+\.\d{2}s')

	def get_mean(image: str):
		values = []
		for _ in range(50):
			values.append(run_tests(image))
		return sum(values)/len(values)

	def run_tests(image: str):
		container = client.containers.run(image, tty=True, volumes = [f'{os.getcwd()}:/app/test'], detach=True)
		container.wait()
		output = container.logs(stderr=False, tail= 1).decode().replace('=','')
		time = regex_seconds.search(output).group()[:-1]
		return float(time)

	images = ['ubuntu_mm', 'py_slim_mm', 'py_alpine_mm']

	for image in images:
		print(f'Computing {image} mean')
		print(f'{image}\'s mean is {get_mean(image)}s')

</details>

The execution of the script returned the following results:
```
Computing ubuntu_mm mean
ubuntu_mm's mean is 0.2506s
Computing py_slim_mm mean
py_slim_mm's mean is 0.28459999999999974s
Computing py_alpine_mm mean
py_alpine_mm's mean is 0.2939999999999999s
```

Surprisingly, the most 'bloated' image was also the fastest one. We should take these results as a grain of salt, because the tests weren't ran on an isolated environment and so they aren't 100% accurate.

#### Updates
When this document was written, Python versions `3.9.9` and even `3.10.1` were available for the `python:3.9-slim` and `python:3.9-alpine`, but the `ubuntu:20.04` image offered only Python up to version `3.9.5`.

#### Final choice
It's clear that in almost all the checks performed the `python:3.9-slim` image was equal or better than the rest, except for the performance one, but the difference was not meaningful enought to end up choosing Ubuntu. Because of this, we decided to use it as the base image of our Dockerfile. We'd reconsider changing it to `python:3.9-alpine` once the distribution of `musllinux` wheels is more extended in the Python community since that would remove the necessity of installing `glibc` and additional libraries in the alpine-based container to be able to install the project dependencies in a faster way.

### Final Dockerfile
We made an effort on following the best practices when creating the Dockerfile:
1. **Creating an unprivileged user**: We created the *music_matcher* user to run the tests. This can difficult privilege scalation attempts when having a container in production.

2. **Adding metadata to the Dockerfile**: We added information about the maintainer and the Dockerfile version that's in use.

3. **Using the minimum possible number of layers**: To achieve this, we used lists of commands -in our example commands separated by `&&`- to minimize the number of `RUN` instructions used.

4. **Optimizing caching image layers**: By placing the layers in a less-likely-to-change to more-likely-to-change order when possible, we take advantage of how Docker caches image layers. When a layer changes, all the following ones must be rebuilt, so to build the minimum number of layers every time the image is built, the layers that change most frequently should be placed at the bottom of the Dockerfile.

As a note, we added the `poetry config virtualenvs.create false` line to the Dockerfile so Poetry doesn't create a virtual environment to install the project dependencies, and those can be used without having to activate the aforementioned environment. Since the container will only be used for running the application, we thought that creating a virtual environment for the application was unnecessary.
