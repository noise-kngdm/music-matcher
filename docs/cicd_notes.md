# CI/CD notes
## Build and push test container GH Action
We developed a [GitHub Action](.github/workflows/build_container.yaml) to build the test container and push it to Docker Hub when the files it depends on are changed on a push to main. To do it, we followed the documentation of the [checkout action](https://github.com/marketplace/actions/checkout), [build and push action](https://github.com/marketplace/actions/build-and-push-docker-images), and [Docker metadata action](https://github.com/marketplace/actions/docker-metadata-action).  

The developed action will build and push to Docker Hub the test container every time the files it depends on have changed on the main branch. Also, the pushed image will have the **main** tag in Docker Hub.

As a note, we created an [Access Token](https://docs.docker.com/docker-hub/access-tokens/) in Docker Hub to use instead of the account's password. This way, Docker Hub lets users monitor what was done using that token, and helps avoid security issues.

## Choosing a CI platform
We had to choose two CI platforms to start automatically executing the unit tests when trying to make any changes to the repository's code. To choose the platforms we used the following criteria:

1. It must have a permanently free version that gives a certain number of credits to open source projects that do not force the user to add billing information.
2. The free credits must be monthly or yearly renewed and the number of credits per month must be as high as possible.
3. It must be easy to integrate with GitHub.
4. It must be easy to install and configure.
5. The platform must be hosted by a third party since we don't have the infrastructure necessary for self-hosting -sorry Jenkins-.
6. It must not have frequent availability problems.

The options considered are the following:

### GitHub Actions
#### Description
A tool developed by GitHub to automate software workflows. It allows developers and organizations not only to perform the typical CI/CD workflows but also to manage their repositories.

#### Analysis
- The use of GitHub Actions is totally free for public repositories so the first two points are covered.
- It's really easy to integrate with GitHub since it's designed by the GitHub team.
- Configuring a GitHub Action is very easy, the developer just needs to upload a YAML file with all the steps to the repository under the `.github/workflows` folder. We have already used a GitHub action to build the container we use to pass the unit tests of the project, so we are already familiarized with its configuration and usage.
- It's hosted by GitHub.
- It had not any recent availability problems that we could notice.

#### Conclusion
GitHub Actions got 6 out of 6 points.

### Semaphore CI
#### Description
A CI/CD tool that [advertises itself](https://semaphoreci.com/product) as a fast tool. It has a free tier and it has good reviews on sites like [g2.com](https://www.g2.com/products/semaphore/reviews). 

#### Analysis
- They have a free tier.
- They give the equivalent of $10 in credits per month to use for free, around 1300 minutes.
- The platform is Cloud-based.

We didn't check the rest of the points since we faced different errors with the service the whole day we tried to use it. For example, when we tried to create an account and configure it we encountered the following error:
[500 semaphore CI](images/semaphoreci.png)

#### Conclusion
We won't consider this option any further because of the availability problems that we faced.

### AppVeyor
#### Description
AppVeyor is another CI/CD platform with a free tier that gives the possibility of having a self-hosted server for free, which isn't what we are looking for but could be interesting for future projects.
#### Analysis
- **Free tier** for open source projects.
- As far as we can tell the only limit the free tier has is that you can only run one concurrent job at a time.
- You can integrate it with GitHub as an OAuth app or as a GitHub app, which requires fewer permissions.
- Its configuration and installation, which is done via the `appveyor.yaml` file is fairly straightforward and has a [Python stack](https://www.appveyor.com/docs/lang/python/) which could be of use for the project.
- It can be either hosted in the cloud or self-hosted.
- It had not any recent availability problems that we could notice.
#### Conclusion
AppVeyor got 6 out of 6 possible points.

### CircleCI
#### Description
A CI/CD tool that allows its free tier to use parallel builds, which is a very interesting feature that the rest of platforms except for GitHub Actions doesn't offer with their free tier.
#### Analysis
- **Free tier** with parallel builds.
- They give 6000 build minutes per month for free.
- The service was designed to be used mainly with GitHub and BitBucket, and [configuring the integration](https://circleci.com/docs/2.0/gh-bb-integration/) is fairly simple.
- CircleCI is [configured](https://circleci.com/docs/2.0/config-intro/#section=configuration) via a YAML file that allows the user to specify all the build steps in an uncomplicated way.
- There's no need to self-host it.
- It had not any recent availability problems that we could notice.
#### Conclusion
CircleCI got 6 out of 6 points, however, since it was the service that was used the most by the rest of the students we decided not to consider it for our project.

### Final choices
After the analysis performed we decided that the best candidates to use as CI/CD platforms for our project are **GitHub Actions** and **AppVeyor**. We discarded the other two options because, althought they could be of use, SemaphoreCI suffered from critical availability problems when we first tried to use it, and CircleCI was used in almost all the rest of the projects.
