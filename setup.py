import os

from setuptools import setup

install_requires = [
    'Flask',
    'Flask-Babel',
]

if os.path.exists('README'):
    with open('README') as f:
        readme = f.read()
else:
    readme = None

setup(
    name='Flask-Table',
    packages=['flask_table'],
    version='0.4.1',
    author='Andrew Plummer',
    author_email='plummer574@gmail.com',
    url='https://github.com/plumdog/flask_table',
    description='HTML tables for use with the Flask micro-framework',
    install_requires=install_requires,
    test_suite='tests',
    tests_require=['flask-testing'],
    long_description=readme,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Operating System :: OS Independent',
        'Framework :: Flask',
    ])
