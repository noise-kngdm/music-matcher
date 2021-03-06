# Music-matcher
Connect with people based on your music tastes.

## Description
If you'd like to attend a show of a band that none of your friends is into, if you feel like meeting a special one who also **loves** that track, or if you just want to get to know new people that enjoy the same bands as you, *music-matcher* is here to help you out.

From your Spotify listening history, *music-matcher* will suggest people who will also be eager to meet you.

## Installation
To install the project, it's necessary to have a **Python3 3.5+** interpreter available in the system.  

### Install the dependencies
#### Install Poetry (required)
First, it's necessary to install [**Poetry**](https://python-poetry.org/), the dependency manager of the project, which ensures that the project is running on an environment with all the required dependencies.  

To install Poetry in a Linux system, it's necessary to run the following command [according to the installation manual](https://python-poetry.org/docs/master/#installation):
```zsh
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 - && \
```  

#### Install the rest of the dependencies
To install the project, clone the repository and `cd` into it. Then install the dependencies and activate the virtual environment that **Poetry** created to be able to run the project in a deterministic way:

```zsh
git clone https://github.con/noise-kngdm/music-matcher;
cd music-matcher;
poetry install;
```  

After this, the project is up and ready to use!

## Usage
To execute the project, **it's necessary to activate the virtual environment** that Poetry prepared for the project after installing the dependencies every time. In order to do that, you only need to execute:
```zsh
poetry shell
```  

**NOTE**:  
To exit the virtual environment you need to either execute `exit` or press `Ctrl+d`, which has the same effect.  

### Checking the programmed entities syntax
To check the syntax of the programmed entities, you only need to `cd` into the root of the project and execute `inv check`.

### Testing the project
To test the different files of the project, it is necessary to have the root folder of the project as the working directory and run `inv test`. **Invoke** will deal with executing *pytest* inside the virtual environment of the project and will show the output properly formated.  

If you only need to execute tests for a class or file, you can use the `-k/--keyword` flag to indicate which tests should be executed, and it will not load the rest of them.

Alternatively, it's possible to use a docker container to run the unit tests. To do that, after having activated the virtual environment set up by Poetry, execute `inv docker`. That command will automatically download the required image and execute the unit tests.
  
## Additional documentation
### User stories
There's a detailed description of every user [here](docs/users.md).  

### Development decisions
There's a detailed explanation of why every tool was selected [here](docs/development_decisions.md).

### Development notes
There's a detailed explanation on why our unit tests comply with the **F.I.R.S.T** principles in the [docs](docs/development_notes.md).

### Infraestructure decisions
On [this document](docs/infrastructure_decisions.md) there is a detailed explanation of the base image used for the test container along with information regarding the principles followed to develop it.

### CI/CD notes
You can read [this document](docs/cicd_notes.md) if you want information regarding the GitHub Action we set up to automatically build and push to [DockerHub](https://hub.docker.com/repository/docker/gonzz/music_matcher) a new test container when necessary. In that document you will also find information regarding the GitHub Action we created to pass the unit tests against different Python versions and in the AppVeyor platform using the test container.
