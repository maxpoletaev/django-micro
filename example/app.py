# -------------------
# Configuration
# -------------------

import os
from django_micro import configure

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/static/'
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

configure(locals(), django_admin=True)


# -------------------
# Imports
# -------------------

from django.shortcuts import render, get_object_or_404
from django.core.management.base import BaseCommand
from django.views.generic import View
from django.http import HttpResponse
from django.test import TestCase
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

@route('', name='index')
def show_index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})


@route('blog/<int:post_id>/', name='post')
def show_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post.html', {'post': post})


@route(r'^regex/(.*)$', regex=True)
def regex_view(request, value):
    return HttpResponse(value)


@route('class-based/')
class ClassBasedView(View):
    def get(self, request):
        return HttpResponse('Hello from class-based view')


# -------------------
# Admin interface
# -------------------

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


route('admin/', admin.site.urls)


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


# --------------------
# Tests
# --------------------

class TestIndexView(TestCase):
    def test_success(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


# -------------------
# Expose application
# -------------------

application = run()
