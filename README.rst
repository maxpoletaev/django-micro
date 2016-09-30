============
Django Micro
============

.. image::
    https://img.shields.io/pypi/v/django-micro.svg
    :target: https://pypi.python.org/pypi/django-micro


Django Micro — Lightweight wrapper for using Django as a microframework and writing small applications in a single file.

**tl;dr:** See an example_ of full-featured application.


Features
========

- Configuration
- Views and routes
- Models (with migrations)
- Custom management commands
- Custom template tags
- Admin interface
- Third party apps


Insallation
===========

.. code-block::

    $ pip install django-micro


Quick start
===========

Create ``app.py`` file with following content.

.. code-block:: python

    from django_micro import configure, route, run
    from django.http import HttpResponse

    DEBUG = True
    configure(locals())


    @route(r'^$', name='index')
    def show_index(request):
        name = request.GET.get('name', 'World')
        return HttpResponse('Hello, {}!'.format(name))


    application = run()

Run the application.

.. code-block::

    $ python app.py runserver

**Note:** Parent directory of ``app.py`` file should be valid python module name. Under the hood Micro adds this directory into ``INSTALLED_APPS`` and use it as normal django application.


Compatibility
=============

We will try to support only latest stable version of Django. This is the only way to keep codebase of django-micro clean, without hacks for many versions of Django.

- **Django version:** >=1.10, <1.11
- **Python version:** 2.7, >=3.4


Run and deployment
==================

On localhost, an application runs with the built-in ``runserver`` command and deploys as a standard WSGI application.

.. code-block::

    $ python app.py runserver
    $ gunicorn app --bind localhost:8000
    $ uwsgi --wsgi-file app.py --http localhost:8000

This behavior provided by single string: ``application = run()``. The strongest magic in django-micro. This is actually just a shortcut to the following code.

.. code-block:: python

    if __name__ == '__main__':
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    else:
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()


Configuration
=============

Call of the ``configure`` function should be placed at top of your application. Before definition views, models and other.

The good way is define all configuration in global namespace and call ``configure`` with ``locals()`` argument. Don't worry, configuration takes only *UPPERCASE* variables.

.. code-block:: python

    from django_micro import configure

    DEBUG = True
    TEMPLATE_DIRS = ['templates']
    configure(locals())


Views and routes
================

Use as decorator:

.. code-block:: python

    from django_micro import route

    @route(r'^$', name='index')
    def show_index(request):
        return HttpResponse('hello')

Use directly:

.. code-block:: python

    def show_index(request):
        return HttpResponse('hello')

    route(r'^$' show_index, name='index')

Also ``route`` may be used with class-based views:

.. code-block:: python

    @route(r'^$', name='index')
    class IndexView(View):
        def get(request):
            return HttpResponse('hello')


Models and migrations
=====================

Micro normally works with models and migrations. Just define model in your ``app.py`` file. If you need migrations, create ``migrations`` directory next to the ``app.py``.

.. code-block:: python

    from django.db import models

    class Post:
      title = models.CharField(max_length=255)

      class Meta:
          app_label = 'blog'

**Note** you always should set ``app_label`` attribute in ``Meta`` of your models. For sample, if application placed as ``blog/app.py``, ``app_label`` must have a ``blog`` value.

For getting ``app_label`` you can use ``get_app_label`` shortcut.

.. code-block:: python

    from django_micro import get_app_label

    class Post:
        class Meta:
            app_label = get_app_label()

You also can place models separately in ``models.py`` file. In this case ``app_label`` is not required. But this is not a micro-way ;)


Related projects
================

- importd_ — Popular implementation of django-as-microframework idea, but over-engineered, magical and not intuitive.

- djmicro_ — Good and lightweight wrapper, but just an experimenal, without support many features out-of-the-box, such as models and migrations. **deprecated**


.. _example: https://github.com/zenwalker/django-micro/tree/master/example
.. _djmicro: https://github.com/apendleton/djmicro
.. _importd: https://github.com/amitu/importd
