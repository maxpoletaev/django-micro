from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.conf.urls import url
import inspect
import django
import os
import sys

__all__ = ['view', 'configure', 'run', 'template', 'urlpatterns']


# -------------------
# Views and routes
# -------------------

urlpatterns = []


def view(pattern, *args, **kwargs):
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

def get_parent_module():
    name = inspect.stack()[2][0].f_locals['__name__']
    return sys.modules[name]


def configure(config_dict={}, app_label=None):
    module = get_parent_module()
    app_label = os.path.basename(os.path.dirname(os.path.abspath(module.__file__)))
    config_dict.setdefault('TEMPLATE_DIRS', ['templates'])

    kwargs = {
        'INSTALLED_APPS': [app_label] + config_dict.pop('INSTALLED_APPS', []),
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
