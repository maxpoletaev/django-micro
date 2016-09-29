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
