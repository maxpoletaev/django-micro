from django_micro import configure, route, template, run, urlpatterns
from django.conf.urls import url
import os


# -------------------
# Configuration
# -------------------

DEBUG = True
STATIC_URL = '/static/'
BASE_DIR = os.path.dirname(__file__)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

CONTEXT_PROCESSORS = [
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

configure(locals())


# -------------------
# Models
# -------------------

from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'example'
        ordering = ('-create_date',)


# -------------------
# Views and routes
# -------------------

from django.shortcuts import render, get_object_or_404


@route(r'^$', name='index')
def show_index(request):
    posts = Post.objects.all()
    name = request.GET.get('name', 'Django')
    return render(request, 'index.html', {'name': name, 'posts': posts})


@route(r'^blog/(\d+)$', name='post')
def show_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post.html', {'post': post})


# -------------------
# Admin interface
# -------------------

from django.contrib import admin


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


urlpatterns.append(url('^admin/', admin.site.urls))


# -------------------
# Template tags
# -------------------

@template.simple_tag
def say_hello(name):
    return 'Hello, {}!'.format(name)


# --------------------
# Management commands
# --------------------

from django.core.management.base import BaseCommand
from django_micro import command


@command('print_hello')
class PrintHelloCommand(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Hello, Django!')


# -------------------
# Expose application
# -------------------

application = run()
