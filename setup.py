from setuptools import setup

setup(
    name='email-parser',
    packages=[
        'email_parser'
    ],
    package_dir={
        'email_parser': 'email_parser'
    },
    test_suite='tests',
    author='Tomaz Muraus',
    author_email='tomaz+pypi@tomaz.me',
)
