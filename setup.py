# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = '0.1'

setup(
    name='django-perobject-permission',
    version=version,
    description="Simple, flexible and scalable Django authorization backend that handle per-object permission management",
    long_description=read('README.md'),
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords=['authorization', 'backends', 'django', 'rules', 'permissions', 'rulez','perobject'],
    author='Lodato Luciano',
    author_email='lodato.luciano@gmail.com',
    url='http://github.com/lodatol/django-perobject-permission',
    license='BSD',
    packages=find_packages(),
    zip_safe=False,
)
