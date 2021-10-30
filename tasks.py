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
