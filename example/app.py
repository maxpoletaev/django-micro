# -------------------
# Configuration
# -------------------

import os
from django_micro import configure

DEBUG = True
STATIC_URL = '/static/'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
# Imports
# -------------------

from django.shortcuts import render, get_object_or_404
from django.core.management.base import BaseCommand
from django.views.generic import View
from django.http import HttpResponse
from django.contrib import admin
from django.db import models

from django_micro import command, route, template, run, get_app_label


# -------------------
# Models
# -------------------

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = get_app_label()
        ordering = ('-create_date',)


# -------------------
# Views and routes
# -------------------

@route(r'^$', name='index')
def show_index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})


@route(r'^blog/(\d+)$', name='post')
def show_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post.html', {'post': post})


@route(r'^class-based$')
class ClassBasedView(View):
    def get(self, request):
        return HttpResponse('Hello from class-based view')


# -------------------
# Admin interface
# -------------------

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


route(r'^admin/', admin.site.urls)


# -------------------
# Template tags
# -------------------

@template.simple_tag
def say_hello(name):
    return 'Hello, {}!'.format(name)


# --------------------
# Management commands
# --------------------

@command('print_hello')
class HelloCommand(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Hello, Django!')


@command()
def print_hello_func(cmd, **options):
    cmd.stdout.write('Hello from function-based command!')


# -------------------
# Expose application
# -------------------

application = run()
