# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE.md for more details.
'''Test Task-Runner.'''

from typing import Optional, TYPE_CHECKING
from invoke import call, task

from proman_github import __version__

if TYPE_CHECKING:
    from invoke import Context

if (
    'dev' in __version__
    or 'a' in __version__
    or 'b' in __version__
    or 'rc' in __version__
):
    part = 'build'
else:
    part = 'patch'


@task
def build(ctx, format=None):  # type: (Context, Optional[str]) -> None
    '''Build wheel package.'''
    if format:
        ctx.run("flit build --format={}".format(format))
    else:
        ctx.run('flit build')


@task(pre=[call(build, format='wheel')])
def dev(ctx):  # type: (Context) -> None
    '''Perform development runtime environment setup.'''
    ctx.run('flit install --symlink --python python3')


@task
def install(
    ctx, symlink=True, dev=False
):  # type: (Context, bool, bool) -> None
    '''Install within environment.'''
    args = []
    if symlink:
        args.append('--symlink')
    if dev:
        args.append('--python=python3')
    ctx.run("flit install {}".format(' '.join(args)))


@task
def version(
    ctx,
    part=part,
    tag=False,
    commit=False,
    message=None,
):  # type: (Context, str, bool, bool, Optional[str]) -> None
    '''Update project version and apply tags.'''
    args = [part]
    if commit:
        args.append('--commit')
    else:
        args.append('--dry-run')
        args.append('--allow-dirty')
        args.append('--verbose')
        print('Add "--commit" to actually bump the version.')
    if tag or message:
        args.append('--tag')
        if message:
            args.append(f"--tag-message '{message}'")
    ctx.run(f"bumpversion {' '.join(args)}")


@task
def publish(ctx):  # type: (Context) -> None
    '''Publish project distribution.'''
    ctx.run('flit publish')


@task
def clean(ctx):  # type: (Context) -> None
    '''Clean project dependencies and build.'''
    paths = ['dist', 'logs']
    paths.append('**/__pycache__')
    paths.append('**/*.pyc')
    paths.append('proman_github.egg-info')
    for path in paths:
        ctx.run("rm -rf {}".format(path))
