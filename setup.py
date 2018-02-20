from setuptools import setup

setup(
    name='django-micro',
    description='Django as a microframework',
    keywords='django microframework',
    py_modules=['django_micro'],
    version='1.6.1',
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
