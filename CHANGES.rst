=========
Changelog
=========

1.8.0 - 2019-10-13
==================

- Django 2.2 support (fixes #20)

1.7.3 - 2019-07-06
==================

- Add missing messages app (fixes #16)

1.7.2 - 2018-08-28
==================

- Use parent directory as the import root (fixes #15)

1.7.1 - 2018-06-30
==================

- AppConfig is now used for app registration
- fix ``--run-syncdb`` migrations (#14)

1.6.1 - 2018-02-20
==================

- add MessageMiddleware to django_admin shortcut

1.6.0 - 2018-02-11
==================

- add shortcut to quick admin interface configuation

1.5.0 - 2017-12-04
==================

- move to Django 2.0
- use the new simplified routing syntax by default

1.4.0 - 2017-03-05
==================

- ``MicroException`` renamed to ``DjangoMicroException``
- using ``BASE_DIR/templates`` as default templates dir
- fix detection application name
- testing support

1.3.0 - 2016-10-17
==================

- add support function-based commands

1.2.0 - 2016-10-08
==================

- support relative and recursive imports
- only way for absolute imports: ``import blog.models`` but not ``import models``

1.1.1 - 2016-10-05
==================

- fix no module named %yourapp%

1.1.0 - 2016-10-01
==================

- ``route`` and ``command`` may be used directly, not only as decorator
- add support class-based views for ``route`` decorator
- add ``get_app_label`` shortcut
- improve python 2.7 compatible

1.0.0 - 2016-09-30
==================

Initial release
