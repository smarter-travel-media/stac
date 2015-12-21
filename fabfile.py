# -*- coding: utf-8 -*-

from fabric.api import (
    hide,
    lcd,
    local,
    task,
    warn_only,
    quiet)


@task
def clean():
    local('rm -rf wheelhouse')
    local('rm -rf dist')
    local('rm -rf build')
    local('rm -rf test/unit/__pycache__')
    local('rm -rf test/integration/__pycache__')

    with lcd('doc'):
        local('make clean')


@task
def docs():
    with lcd('doc'):
        local('make html')


@task
def lint():
    with warn_only():
        local('pylint --rcfile .pylintrc stac')


@task
def coverage():
    with quiet():
        local('coverage run --source stac ./.env/bin/py.test test/unit')

    with hide('running'):
        local("coverage report  --show-missing")


@task
def push():
    local('git push origin')


@task
def push_tags():
    local('git push --tags origin')


@task
def pypi():
    local('python setup.py sdist bdist_wheel')
    local('twine upload dist/*')
