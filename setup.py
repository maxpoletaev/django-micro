import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-micro',
    description='Django as a microframework',
    long_description=read('README.rst'),
    keywords='django microframework',
    py_modules=['django_micro'],
    version='1.7.3',
    author='Max Poletaev',
    author_email='max.poletaev@gmail.com',
    url='https://github.com/zenwalker/django-micro',
    license='BSD',
    install_requires=[
        'django>=2.0,<2.1',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
    ],
)
