from importlib import import_module
import inspect
import sys
import os

import django
from django.apps import AppConfig
from django.conf import settings
from django.core import management
from django.template import Library
from django.urls import path, re_path
from django.core.management.base import BaseCommand
from django.core.exceptions import ImproperlyConfigured

__all__ = ['command', 'configure', 'run', 'route', 'template', 'get_app_label']

register = template = Library()
urlpatterns = []

_parent_module = None
_app_config = None
_commands = {}


def _create_app(stack):
    parent_module = sys.modules[stack[1][0].f_locals['__name__']]
    parent_module_dir = os.path.dirname(os.path.abspath(parent_module.__file__))

    # use parent directory of application as import root
    sys.path[0] = os.path.dirname(parent_module_dir)

    app_module = os.path.basename(parent_module_dir)
    entrypoint = '{}.{}'.format(app_module, os.path.basename(parent_module.__file__).split('.')[0])

    # allow relative import from app.py
    parent_module.__package__ = app_module
    import_module(app_module)

    # allow recursive import app.py
    if parent_module.__name__ != app_module:
        sys.modules[entrypoint] = parent_module

    class MicroAppConfig(AppConfig):
        module = app_module
        label = app_module
        name = app_module

        def import_models(self):
            super().import_models()
            if self.models_module is None:
                self.models_module = parent_module

    globals().update(
        _app_config=MicroAppConfig,
        _parent_module=parent_module,
    )


def get_app_label():
    if _app_config is None:
        raise ImproperlyConfigured(
            "Application label is not detected. "
            "Check whether the configure() was called.")
    return _app_config.label


def route(pattern, view_func=None, regex=False, *args, **kwargs):
    path_func = re_path if regex else path

    def decorator(view_func):
        if hasattr(view_func, 'as_view'):
            view_func = view_func.as_view()

        urlpatterns.append(path_func(pattern, view_func, *args, **kwargs))
        return view_func

    # allow use decorator directly
    # route('blog/', show_index)
    if view_func:
        return decorator(view_func)

    return decorator


def configure(config_dict={}, django_admin=False):
    _create_app(inspect.stack())  # load application from parent module

    if 'BASE_DIR' in config_dict:
        config_dict.setdefault('TEMPLATE_DIRS', [os.path.join(config_dict['BASE_DIR'], 'templates')])

    if django_admin:
        _configure_admin(config_dict)

    django_config = {
        'INSTALLED_APPS': ['django_micro._app_config'] + config_dict.pop('INSTALLED_APPS', []),
        'ROOT_URLCONF': __name__,
        'TEMPLATES': [{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': config_dict.pop('TEMPLATE_DIRS', []),
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': config_dict.pop('CONTEXT_PROCESSORS', []),
                'builtins': [__name__],
            },
        }],
    }

    django_config.update({key: val for key, val in config_dict.items() if key.isupper()})
    settings.configure(**django_config)
    django.setup()


def _configure_admin(config_dict):
    admin_deps = {
        'INSTALLED_APPS': [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
        ],
        'MIDDLEWARE': [
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.middleware.security.SecurityMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ],
        'CONTEXT_PROCESSORS': [
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    }

    for key, value in admin_deps.items():
        prev_value = config_dict.get(key, [])
        config_dict[key] = value + prev_value

    config_dict.setdefault('STATIC_URL', '/static/')


def _patch_get_commands():
    django_get_commands = management.get_commands

    def patched_get_commands():
        commands = django_get_commands()
        commands.update(_commands)
        return commands

    patched_get_commands.patched = True
    management.get_commands = patched_get_commands


def command(name=None, command_cls=None):
    if not getattr(management.get_commands, 'patched', False):
        _patch_get_commands()

    if inspect.isfunction(name):
        # Shift arguments if decroator called without brackets
        command_cls = name
        name = None

    def decorator(command_cls):
        command_name = name

        if inspect.isclass(command_cls):
            command_instance = command_cls()
        else:
            # transform function-based command to class
            command_name = name or command_cls.__name__
            command_instance = type('Command', (BaseCommand,), {'handle': command_cls})()

        if not command_name:
            raise DjangoMicroException("Class-based commands requires name argument.")

        # Hack for extracting app name from command (https://goo.gl/1c1Irj)
        command_instance.rpartition = lambda x: [_app_config.module]

        _commands[command_name] = command_instance
        return command_cls

    # allow use decorator directly
    # command('print_hello', PrintHelloCommand)
    if command_cls:
        return decorator(command_cls)

    return decorator


class DjangoMicroException(Exception):
    pass


def run():
    if not settings.configured:
        raise ImproperlyConfigured("You should call configure() after configuration define.")

    if _parent_module.__name__ == '__main__':
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    else:
        from django.core.wsgi import get_wsgi_application
        return get_wsgi_application()
