from django.conf import settings
from django.conf.urls import url
from django.shortcuts import render
import django
import sys

app_name = 'django_micro'
sys.modules[app_name] = sys.modules[__name__]


# -------------------
# Views
# -------------------


def show_index(request):
    name = request.GET.get('name', 'World')
    return render(request, 'index.html', {'name': name})


# -------------------
# Configuration
# -------------------


urlpatterns = [
    url(r'^$', show_index, name='form_action'),
]

django_settings = {
    'INSTALLED_APPS': [app_name],
    'ROOT_URLCONF': app_name,
    'ALLOWED_HOSTS': [],
    'DEBUG': True,
    'TEMPLATES': [{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
    }],
}

settings.configure(**django_settings)
django.setup()


# -------------------
# Bootstrap
# -------------------


if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
else:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
