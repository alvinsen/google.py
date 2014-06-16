# coding=utf8

from setuptools import setup
from g import __version__


setup(
    name='g',
    version=__version__,
    author='hit9',
    author_email='nz2324@126.com',
    license='BSD',
    packages=['g'],
    zip_safe=False,
    include_package_data=True,
    entry_points={
        'console_scripts': ['google=g.g:main']
    },
    install_requires=['requests', 'gevent']
)
