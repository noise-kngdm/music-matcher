# Music-matcher
Connect with people based on your music tastes.

## Description
If you'd like to attend a show of a band that none of your friends is into, if you feel like meeting a special one who also **loves** that track, or if you just want to get to know new people that enjoy the same bands as you, *music-matcher* is here to help you out.

From your Spotify listening history, *music-matcher* will suggest people who will also be eager to meet you.

## Installation
To install the project, it's necessary to have a **Python3 3.5+** interpreter available in the system.  

### Install the dependencies
#### Install Poetry (required)
First it's necessary to install [**Poetry**](https://python-poetry.org/), the dependency manager of the project, which ensures that the project is running on an environment with all the required dependencies.  

To install Poetry in a Linux system, it's necessary to run the following command [according with the installation manual](https://python-poetry.org/docs/master/#installation):
```zsh
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
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
  
## Additional documentation
### User stories
There's a detailed description of every user [here](www.github.com/noise-kngdm/music-matcher/docs/users.md).  

### Development decisions
There's a detailed explanation of why every tool was selected [here](www.github.com/noise-kngdm/music-matcher/docs/development_decisions.md).
