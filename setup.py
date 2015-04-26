# coding=utf8

from setuptools import setup
from google import __version__


setup(
    name='google.py',
    version=__version__,
    author='hit9',
    author_email='nz2324@126.com',
    license='BSD',
    packages=['google'],
    zip_safe=False,
    include_package_data=True,
    entry_points={
        'console_scripts': ['google=google.g:main']
    },
    install_requires=['requests==2.5.0', 'gevent==1.0.1']
)
