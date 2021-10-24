# Music-matcher
Connect with people based on your music tastes.

## Description
If you'd like to attend a show of a band that none of your friends is into, if you feel like meeting a special one who also **loves** that track, or if you just want to get to know new people that enjoy the same bands as you, *music-matcher* is here to help you out.

From your Spotify listening history, *music-matcher* will suggest people who will also be eager to meet you.

## Additional documentation
### User stories
There's a detailed description of every user [here](www.github.com/noise-kngdm/music-matcher/docs/users.md).  

### Development decisions
#### Programming language: **Python**
We chose Python because of its broad community -which makes the learning path smoother-, its readable and syntactic-sugar-prone coding style, OS compatibility, and the high number of well-maintained open-source libraries available for the users.  

### Task runner: **Invoke**
[Invoke](https://www.pyinvoke.org/) is a task runner written in Python that allows defining your tasks in a pythonic way, while having an invocation style similar to *GNU Make*, which is very convenient for CLI-accustomed users. It is an open-source and well-maintained project and has an [extensive documentation](https://docs.pyinvoke.org/en/stable/) with lots of examples that make it very easy to start using it.  

### Package and dependency manager: **Poetry**
[Poetry](https://python-poetry.org/) is a packaging and dependency manager. It can resolve the multiple dependency constraints of a project if there's any possible solution and ease the task of working on a shared repository by ensuring that every developer is working with the same environment. It also supports building pure python wheels and publishing them.
It also has a very easy-to-use command-line interface with tab completion and has a broad user-base within the Python community.

