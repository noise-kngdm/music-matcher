# CI/CD notes
## Build and push test container GH Action
We developed a [GitHub Action](.github/workflows/build_container.yaml) to build the test container and push it to Docker Hub when the files it depends on are changed on a push to main. To do it, we followed the documentation of the [checkout action](https://github.com/marketplace/actions/checkout), [build and push action](https://github.com/marketplace/actions/build-and-push-docker-images), and [Docker metadata action](https://github.com/marketplace/actions/docker-metadata-action).  

The developed action will build and push to Docker Hub the test container every time the files it depends on have changed on the main branch. Also, the pushed image will have the **main** tag in Docker Hub.

As a note, we created an [Access Token](https://docs.docker.com/docker-hub/access-tokens/) in Docker Hub to use instead of the account's password. This way, Docker Hub lets users monitor what was done using that token, and helps avoid security issues.
