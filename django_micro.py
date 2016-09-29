from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.conf.urls import url
import inspect
import django
import os
import sys

__all__ = ['command', 'configure', 'run', 'route', 'template', 'urlpatterns']


# -------------------
# Views and routes
# -------------------

urlpatterns = []


def route(pattern, *args, **kwargs):
    def wrapper(view_fn):
        kwargs.setdefault('name', view_fn.__name__)
        urlpatterns.append(url(pattern, view_fn, *args, **kwargs))
        return view_fn
    return wrapper


# -------------------
# Template tags
# -------------------

from django.template import Library
register = template = Library()


# --------------------
# Configuration
# --------------------

def get_parent_module(offset=0):
    name = inspect.stack()[2 + offset][0].f_locals['__name__']
    return sys.modules[name]


def get_app_label():
    module = get_parent_module(1)
    return os.path.basename(os.path.dirname(os.path.abspath(module.__file__)))


def configure(config_dict={}):
    config_dict.setdefault('TEMPLATE_DIRS', ['templates'])

    kwargs = {
        'INSTALLED_APPS': [get_app_label()] + config_dict.pop('INSTALLED_APPS', []),
        'ROOT_URLCONF': __name__,
        'TEMPLATES': [{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': config_dict.pop('TEMPLATE_DIRS'),
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': config_dict.pop('CONTEXT_PROCESSORS', []),
                'builtins': [__name__],
            },
        }],
    }

    kwargs.update({key: val for key, val in config_dict.items() if key.isupper()})
    settings.configure(**kwargs)
    django.setup()


# --------------------
# Management commands
# --------------------

from django.core import management
_commands = {}


def patch_get_commands():
    django_get_commands = management.get_commands

    def patched_get_commands():
        commands = django_get_commands()
        commands.update(_commands)
        return commands

    patched_get_commands.patched = True
    management.get_commands = patched_get_commands


def command(name):
    app_label = get_app_label()
    if not getattr(management.get_commands, 'patched', False):
        patch_get_commands()

    def wrapper(command_cls):
        command_instance = command_cls()
        # very dirty hack for extracting app name
        # from command (via https://goo.gl/1c1Irj)
        command_instance.rpartition = lambda x: [app_label]
        _commands[name] = command_instance
        return command_cls

    return wrapper


# --------------------
# Bootstrap
# --------------------

def run():
    parent = get_parent_module()

    if not settings.configured:
        msg = "You should call configure() after configuration define."
        raise ImproperlyConfigured(msg)

    if parent.__name__ == '__main__':
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    else:
        from django.core.wsgi import get_wsgi_application
        return get_wsgi_application()
