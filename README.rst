============
Django Micro
============

.. image::
    https://img.shields.io/pypi/v/django-micro.svg
    :target: https://pypi.python.org/pypi/django-micro


Django Micro — Lightweight wrapper for usgin Django as microframework and writing small application in single file.


Features
========

- Configuration
- Views and routes
- Models (with migrations)
- Custom management commands
- Custom template tags
- Admin interface
- Third party apps

See example_ with usign all of this features.


Insallation
===========

.. code-block::

    $ pip install django-micro


Usage
=====

.. code-block:: python

    from django_micro import configure, route, run
    from django.shortcuts import render

    DEBUG = True
    configure(locals())


    @route(r'^$', name='index')
    def show_index(request):
        name = request.GET.get('name', 'World')
        return render(request, 'index.html', {'name': name})


    # expose wsgi application
    application = run()


On localhost application runs with built-in ``runserver`` command and deploy as standard WSGI application. No difference, no magick.

.. code-block::

    $ python app.py runserver
    $ gunicorn app --bind localhost:8000


Related projects
================

- importd_ — Popular implementation django-as-microframework idea, but over-engineered, magickal and not intuitive.
- djmicro_ — Good and lightweight wrapper, but just experiment, without support many features out-of-the-box, such as models and migrations. **Deprecated**.


.. _example: https://github.com/zenwalker/django-micro/tree/master/example
.. _djmicro: https://github.com/apendleton/djmicro
.. _importd: https://github.com/amitu/importd
