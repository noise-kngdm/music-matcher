# CI/CD notes
## Build and push test container GH Action
We developed a [GitHub Action](.github/workflows/build_container.yaml) to build the test container and push it to Docker Hub when the files it depends on are changed on a push to main or a pull request to main. To do it, we followed the documentation of the [checkout action](https://github.com/marketplace/actions/checkout), [build and push action](https://github.com/marketplace/actions/build-and-push-docker-images), and [Docker metadata action](https://github.com/marketplace/actions/docker-metadata-action).  

The developed action will build and push to Docker Hub the test container every time the files it depends on have changed either on the main branch or in a pull request. Also, to help differentiate between these changes, the uploaded image will have a **different tag** depending on if it was built after pushing to main -it will have the **main** tag- or if it was built for a pull request -where it will have the **pr-<PR number>** tag. This will help to know which image version the tests must be run against.

As a note, we created an [Access Token](https://docs.docker.com/docker-hub/access-tokens/) in Docker Hub to use instead of the account's password. This way, Docker Hub lets users monitor what was done using that token, and helps avoid security issues.
