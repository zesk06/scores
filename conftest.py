#!/usr/bin/env python
# encoding: utf-8


def pytest_addoption(parser):
    parser.addoption('--selenium', action='store_true', dest='doselenium',
                     help='to run selenium tests, '
                          'require a localhost:8080 webserver to be launched')