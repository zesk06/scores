"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
"""

import os
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open

HERE = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='scores',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.0.0',

    description='A python flask app to manage board game scores',
    LONG_DESCRIPTION=LONG_DESCRIPTION,

    # The project's main homepage.
    url='https://github.com/zesk06/scores',

    # Author details
    author='Nicolas Rouviere',
    author_email='zesk06@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Web',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='boardgame',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['scores', 'tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'flask==0.11.1',
        'apipkg==1.4',
        'autopep8==1.2.4',
        'click==6.6',
        'execnet==1.4.1',
        'Flask==0.11.1',
        'Flask-Login==0.3.2',
        'gunicorn==19.6.0',
        'itsdangerous==0.24',
        'Jinja2==2.8',
        'jsonpickle==0.9.3',
        'MarkupSafe==0.23',
        'mongokit==0.9.1.1',
        'pbr==1.10.0',
        'py==1.4.31',
        'PyYAML==3.11',
        'python-dateutil==1.5',
        'requests==2.8.1',
        'six==1.10.0',
        'Werkzeug==0.11.11',
        # pymongo 2.8.0 is the most we can have to have mongokit to work',
        'pymongo==2.8.0',
        ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': [
            'check-manifest',
            'pep8==1.7.0',
            'ipython<6',
            'pylint==1.8.2',
            'pytest==3.0.2',
            'pytest-cache==1.0',
            'pytest-cov==2.3.1',
            'pytest-pep8==1.0.6',
            'selenium==2.52.0',
            'stevedore==1.17.1',
            'virtualenv==15.0.3',
            'virtualenv-clone==0.2.6',
            'virtualenvwrapper==4.7.2'
        ],
        'test': ['coverage',
                 'coverage==4.2'
            ],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'sample': ['package_data.dat'],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    },
)
