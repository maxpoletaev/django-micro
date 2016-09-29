from django_micro import configure, view, template, run
from django.shortcuts import render

DEBUG = True
configure(locals())


@view(r'^$', name='index')
def show_index(request):
    name = request.GET.get('name', 'Django')
    return render(request, 'index.html', {'name': name})


@template.simple_tag
def say_hello(name):
    return 'Hello, {}!'.format(name)


application = run()
