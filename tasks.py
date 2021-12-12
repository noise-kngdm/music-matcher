"""
Tasks file for the project.

Use as: 'inv <task>'
To list all the available tasks run: 'inv --list'
"""
from invoke import task


def poetry_run(ctx, command: str, pty: bool = True):
    """
    Runs a command inside poetry's venv.

    Parameters
    ----------
    command : str
        The command that will be ran.
    """
    ctx.run(f'poetry run {command}', pty=pty)


@task(help={'style': 'Analyze code style too'})
def check(ctx, style=False):
    """
    Checks that the syntax of the project entities is valid running a SCA tool.

    Parameters
    ----------
    style : bool
        If code style will be checked too.
    """
    pylint_check = ['music_matcher', 'tasks.py']
    poetry_run(ctx, 'pylint ' + ('-E ' if not style else '') + ' '.join(pylint_check))


@task(help={'keyword': 'Filter the test list.',
            'capture_output': 'Print stdout and stderr.'})
def test(ctx, keyword='', capture_output=False):
    """
    Run the unit tests.

    Parameters
    ----------
    keyword : str
        The keyword that will be used to select which tests will be ran. If its
        empty, all tests will be ran.
    capture_output : bool
        If set to True, pytest will capture and show stdout and stderr too.
    """
    poetry_run(ctx, f'poetry run pytest {"-k keyword" if keyword else ""} '
               f'{""if not capture_output else "-rP"}')


@task()
def install(ctx):
    """
    Install the required dependencies.
    """
    ctx.run('poetry install', pty=True)
