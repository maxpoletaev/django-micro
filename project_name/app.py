import os
import sys

BASE_DIR = os.path.dirname(__file__)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '{{ secret_key }}')


# -------------------
# Views
# -------------------

from django.shortcuts import render


def show_index(request):
    name = request.GET.get('name', 'World')
    return render(request, 'index.html', {'name': name})


# -------------------
# Configuration
# -------------------

from django.conf.urls import url
from django.conf import settings


urlpatterns = [
    url(r'^$', show_index),
]

settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    SECRET_KEY=SECRET_KEY,
    STATIC_URL='/static/',
    INSTALLED_APPS=[
        'django.contrib.staticfiles',
    ],
    STATICFILES_DIRS=[
        os.path.join(BASE_DIR, 'static'),
    ],
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
    }],
)


# -------------------
# Bootstrap
# -------------------

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
else:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
