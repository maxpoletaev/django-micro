from setuptools import setup

setup(
    name='django-micro',
    description='Django as microframework',
    keywords='django microframework',
    py_modules=['django_micro'],
    version='1.3.0',
    author='Max Poletaev',
    author_email='max.poletaev@gmail.com',
    url='https://github.com/zenwalker/django-micro',
    license='BSD',
    install_requires=[
        'django>=1.10,<1.11',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
    ],
)
