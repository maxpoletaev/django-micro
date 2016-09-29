# Django Micro

Use Django as microframework. Write small application in single file.


## Short example

```python
from django_micro import configure, view, run
from django.shortcuts import render

DEBUG = True
configure(locals())


@view(r'^$', name='index')
def show_index(request):
    name = request.GET.get('name', 'World')
    return render(request, 'index.html', {'name': name})


application = run()
```

On localhost application runs with built-in `python app.py runserver` command and deploy as standard WSGI application. No difference, no magick.


## What works

 - Configuration
 - Views and routes
 - Models (with migrations)
 - Custom management commands
 - Custom template tags
 - Admin interface
 - Third party apps

See [example](/example/) with usign all of this features.
