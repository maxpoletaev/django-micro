============
Django Micro
============

.. image::
    https://img.shields.io/pypi/v/django-micro.svg
    :target: https://pypi.python.org/pypi/django-micro

.. image::
    https://img.shields.io/badge/status-stable-brightgreen.svg

Django Micro — Lightweight wrapper for using Django as a microframework and writing small applications in a single file.

**tl;dr:** See an example_ of full-featured application.


What's works
============

- `Configuration`_
- `Views and routes`_
- `Models and migrations`_
- `Management commands`_
- `Custom template tags`_
- `Testing`_
- Admin interface
- Third party apps


Installation
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

Micro based only on latest stable version of Django. This is the only way to keep codebase of django-micro clean, without hacks for many versions of Django.

- **Django version:** >=1.10, <1.11
- **Python version:** 2.7, >=3.4


Run and deployment
==================

On localhost, an application runs with the built-in ``runserver`` command and deploys as a standard WSGI application.

.. code-block::

    $ python app.py runserver
    $ gunicorn example.app --bind localhost:8000
    $ uwsgi --module example.app --http localhost:8000

This behaviour provided by single string: ``application = run()``. The strongest magic in django-micro. This is actually just a shortcut to the following code.

.. code-block:: python

    if __name__ == '__main__':
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    else:
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()


Configuration
=============

Call of the ``configure`` function should be placed at top of your application. Before definition views, models and imports another modules. Yes, it may violate PEP8. But this is the only way. You can't import any model from another application if Django is not configured.

The good way is define all configuration in global namespace and call ``configure`` with ``locals()`` argument. Don't worry, configuration takes only *UPPERCASE* variables.

.. code-block:: python

    from django_micro import configure

    DEBUG = True
    TEMPLATE_DIRS = ['templates']

    configure(locals())


Views and routes
================

Routing is wrapped in single function ``route``. You can use it as decorator.

.. code-block:: python

    from django_micro import route

    @route(r'^$', name='index')
    def show_index(request):
        return HttpResponse('hello')

Or use directly.

.. code-block:: python

    def show_index(request):
        return HttpResponse('hello')

    route(r'^$' show_index, name='index')

Also ``route`` may be used with class-based views.

.. code-block:: python

    @route(r'^$', name='index')
    class IndexView(View):
        def get(request):
            return HttpResponse('hello')

    # or directly
    route(r'^$', IndexView.as_view(), name='index')

You always can access to ``urlpatterns`` for using the low-level API.

.. code-block:: python

    from django.conf.urls import url
    import django_micro as micro

    micro.urlpatterns += [
        url(r'^$', mainpage, name='mainpage'),
    ]


**Note:** You can include third-party apps into Micro ``urlpatterns``, but currently can't use Micro as third-party app. Micro — is singleton. You can't create more that one instance of it.


Models and migrations
=====================

Micro normally works with models and migrations. Just define model in your ``app.py`` file. If you need migrations, create ``migrations`` directory next to the ``app.py`` and call ``python app.py makemigrations``.

.. code-block::

    blog
    ├── __init__.py
    ├── app.py
    └── migrations
        ├── __init__.py
        └── 0001_initial.py

.. code-block:: python

    from django.db import models

    class Post(models.Model):
        title = models.CharField(max_length=255)

        class Meta:
            app_label = 'blog'

**Note:** You always need to set ``app_label`` attribute in ``Meta`` of your models. For example, if application placed in ``blog/app.py``, app_label should be ``blog``.

For getting ``app_label`` you can use ``get_app_label`` shortcut.

.. code-block:: python

    from django_micro import get_app_label
    from django.db import models

    class Post(models.Model):
        class Meta:
            app_label = get_app_label()

You also can place models separately in ``models.py`` file. In this case ``app_label`` is not required. But this is not a micro-way ;)


Management commands
===================

Now you can create any management cli command without creating file in ``yourapp/management/commands``. Just defne command class in your ``app.py`` and wrap it to ``@command`` decorator.

.. code-block:: python

    from django.core.management.base import BaseCommand
    from django_micro import command

    @command('print_hello')
    class PrintHelloCommand(BaseCommand):
        def handle(self, *args, **options):
            self.stdout.write('Hello, Django!')

You also can create function-based commands.

.. code-block:: python

    from django_micro import command

    @command
    def print_hello(cmd, **options):
        cmd.stdout.write('Hello, Django!')

Unfortunately the ``command`` decorator uses a few dirty hacks for commands registration. But everything works be fine if you don't think about it ;)


Custom template tags
====================

Use ``template`` for register template tags. It works same as a ``register`` object in tag library file.

.. code-block:: python

    from django_micro import template

    @template.simple_tag
    def print_hello(name):
        return 'Hello, {}!'

    @template.filter
    def remove_spaces(value):
        return value.replace(' ', '')


You don't need to use the ``load`` tag. All template tags are global.


Testing
=======

No magick. Use built-in test cases.

.. code-block:: python

    from django.test import TestCase

    class TestIndexView(TestCase):
        def test_success(self):
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)

To run tests which defined in app.py use the following command:

.. code-block::

    $ python app.py test __main__


Who uses django-micro
=====================

- `storagl <https://github.com/zenwalker/storagl>`_ — simple storage for screenshots and other shared files with short direct links


Related projects
================

- importd_ — Popular implementation of django-as-microframework idea, but over-engineered, in my opinion, and magical.

- djmicro_ — Good and lightweight wrapper. I took a few ideas from there. But just an experimental, undocumented, less functional and **deprecated**.


.. _example: https://github.com/zenwalker/django-micro/tree/master/example
.. _djmicro: https://github.com/apendleton/djmicro
.. _importd: https://github.com/amitu/importd
