import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='OnlineNIC',
    version='0.1.0',
    url='http://github.com/kolanos/onlinenic',
    license='MIT',
    author='Michael Lavers',
    author_email='kolanos@gmail.com',
    description='A simple wrapper for the OnlineNIC API.',
    long_description=read('README.rst'),
    py_modules=['onlinenic'],
    platforms='any',
    install_requires=['BeautifulSoup'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
