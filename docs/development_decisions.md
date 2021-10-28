# Development decisions
The reasons why every tool used in the project was chosen are detailed in this file.

## Programming language: **Python**
We chose Python because of its broad community -which makes the learning path smoother-, its readable and syntactic-sugar-prone coding style, OS compatibility, and the high number of well-maintained open-source libraries available for the users.  

## Task runner: **Invoke**
[Invoke](https://www.pyinvoke.org/) is a task runner written in Python that allows defining your tasks in a pythonic way, while having an invocation style similar to *GNU Make*, which is very convenient for CLI-accustomed users. It is an open-source and well-maintained project and has an [extensive documentation](https://docs.pyinvoke.org/en/stable/) with lots of examples that make it very easy to start using it.  

## Package and dependency manager: **Poetry**
[Poetry](https://python-poetry.org/) is a packaging and dependency manager. It can resolve the multiple dependency constraints of a project if there's any possible solution and ease the task of working on a shared repository by ensuring that every developer is working with the same environment. It also supports building pure python wheels and publishing them.
It also has a very easy-to-use command-line interface with tab completion and has a broad user-base within the Python community.
