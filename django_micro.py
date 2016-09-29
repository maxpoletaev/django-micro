from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.conf.urls import url
import inspect
import django
import sys


# -------------------
# Views and routes
# -------------------

urlpatterns = []


def view(pattern, name=None, *args, **kwargs):
    def wrapper(view_fn):
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
    return name, sys.modules[name]


def configure(config_dict={}):
    kwargs = {
        'ROOT_URLCONF': __name__,
        'TEMPLATES': [{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'OPTIONS': {'builtins': [__name__]},
            'DIRS': ['templates'],
        }],
    }

    kwargs.update({key: val for key, val in config_dict.items() if key.isupper()})
    settings.configure(**kwargs)
    django.setup()


# --------------------
# Bootstrap
# --------------------

def run():
    parent_name, _ = get_parent_module()

    if not settings.configured:
        msg = "You should call configure() after configuration define."
        raise ImproperlyConfigured(msg)

    if parent_name == '__main__':
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    else:
        from django.core.wsgi import get_wsgi_application
        return get_wsgi_application()
