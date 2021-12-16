# Development decisions
The reasons why every tool used in the project was chosen are detailed in this file.

## Programming language: **Python**
We chose Python because of its broad community -which makes the learning path smoother-, its readable and syntactic-sugar-prone coding style, OS compatibility, and the high number of well-maintained open-source libraries available for the users.  

## External libraries
The criteria we will use to select every external library is the following:

1. Ease of use.
    The library must be easy to use and well documented to facilitate setting it up and having a maintainable code.

2. Active and frequent development.
    It is crucial that the libraries used are regularly updated and patched to have up-to-date code that complies with the latest software requirements. If we chose any poorly maintained tool, we'd risk having to refactor that code to use a newer tool in the near future.

3. Secure.
    Nowadays it is imperative to always develop secure code and use secure libraries -the recent [Log4J](https://thehackernews.com/2021/12/extremely-critical-log4j-vulnerability.html) critical vulnerability is a good example of that-. Because of this, we will try to choose libraries that have not had notable security flaws in the past.

4. Facilitates having the best practices of the programming language of choice.
    We will try to choose libraries that are PEP compliant to achieve the goal of only developing quality code.

### Task runner: **Invoke**
[Invoke](https://www.pyinvoke.org/) is a task runner written in Python that allows defining your tasks in a pythonic way, while having an invocation style similar to *GNU Make*, which is very convenient for CLI-accustomed users. It is an open-source and well-maintained project and has an [extensive documentation](https://docs.pyinvoke.org/en/stable/) with lots of examples that make it very easy to start using it.  

### Package and dependency manager: **Poetry**
[Poetry](https://python-poetry.org/) is a packaging and dependency manager. It can resolve the multiple dependency constraints of a project if there's any possible solution and ease the task of working on a shared repository by ensuring that every developer is working with the same environment. It also supports building pure python wheels and publishing them.
It also has a very easy-to-use command-line interface with tab completion and has a broad user-base within the Python community.  

### Test framework: **Pytest**
When choosing a test framework we primarily considered [Unittest](https://docs.python.org/3/library/unittest.html) and [Pytest](https://docs.pytest.org/en/6.2.x/). We think that Pytest is more straightforward to use since Unittest needs more module importing and class-defining boilerplate, which can be a hassle to work with. Pytest has several plugins which can come in handy for later stages of the project, for example, one that allows users to generate HTTP reports using the *pytest-http* plugin. None of them have had remarkable security issues in the last years, so this point is a draw. As for the last point, we think that pytest would be a better fit because using a context manager to mock an object -as unittest does- can make the code less readable when having to mock different objects because of the nested `with` statements.  

Because of these reasons, we have decided to use **Pytest**.


### Assertions library: **Assertpy**
To choose an assertion library we considered [Assertpy](https://pypi.org/project/assertpy/) and [Grappa](https://pypi.org/project/grappa/). Both of them have a similar syntax which makes reading the assertion statements very similar to reading natural language, however, as `Grappa` states in its documentation, it is not a mature project and, even though that shouldn't be an issue, we prefer to use a more established library to deal with such a crucial part of the test suite.

### YAML parser: **pyyaml**
Because of the data model we chose for #20, we needed to include a YAML parser to be able to read the file with information about the music genres and the relationship between them. We considered using  [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation) and [ruamel.yaml](https://yaml.readthedocs.io/en/latest/overview.html), which are the only suitable options that we found. `ruamel.yaml` is a fork of `PyYAML` whose main difference is that it has support for `YAML 1.2`, however [it's planned to be supported by PyYAML in version 6.1](https://github.com/yaml/pyyaml/projects/9#card-69485758). Because the support of `YAML 1.2` is not imperative for this project and both projects are very similar, we have chosen **pyyaml** mainly because it has a broader user and developer base.
