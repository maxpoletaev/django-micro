# Django Micro

Django application in single file.

## Usage

### Start project from template

```
django-admin startproject my_project \
--template=https://github.com/zenwalker/django-micro/archive/master.zip
```

### Run

```
$ python my_project/app.py runserver
```

## Cookbook

### Custom template tags

 1. Add template tags section to `app.py`

    ```python
    # -------------------
    # Template tags
    # -------------------

    from django.template import Library
    register = Library()


    @register.simple_tag
    def hello(name):
        return 'Hello, {}'.format(name)
    ```

 2. Add `builtins` option to template configuration

    ```python
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'builtins': [__name__],
        },
    }]
    ```

 3. Just call tag in template (without `load`)

    ```html
    <html>
      <body>
        <h1>{% hello "John" %}</h1>
      </body>
    </html>
    ```
