# -*- coding: utf-8 -*-

from fabric.api import (
    lcd,
    local,
    task)


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
