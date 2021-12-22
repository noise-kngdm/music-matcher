"""
Tasks file for the project.

Use as: 'inv <task>'
To list all the available tasks run: 'inv --list'
"""
from invoke import task


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
    ctx.run('pylint ' + ('-E ' if not style else '') + ' '.join(pylint_check))


@task(help={'keyword': 'Filter the test list.',
            'capture_output': 'Print stdout and stderr.'})
def test(ctx, keyword='', capture_output=True):
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
    args = []
    if keyword:
        args.append(f'k {keyword}')

    ctx.run(' -'.join(['pytest'] + args), pty=capture_output)


@task
def docker(ctx):
    """
    Run the unit tests inside a container.
    """
    ctx.run("docker run -t -v $(pwd):/music_matcher/test gonzz/music_matcher", pty=True)
