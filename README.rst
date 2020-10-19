============
Choices Enum
============


.. image:: https://img.shields.io/pypi/v/choicesenum.svg
        :target: https://pypi.python.org/pypi/choicesenum

.. image:: https://travis-ci.org/loggi/python-choicesenum.svg?branch=master
        :target: https://travis-ci.org/loggi/python-choicesenum

.. image:: https://readthedocs.org/projects/python-choicesenum/badge/?version=latest
        :target: https://python-choicesenum.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/loggi/python-choicesenum/badge.svg?branch=master
        :target: https://coveralls.io/github/loggi/python-choicesenum?branch=master


Python's Enum with extra powers to play nice with labels and choices fields.

* Free software: BSD license
* Documentation: https://python-choicesenum.readthedocs.io.

------------
Installation
------------

Install ``choicesenum`` using pip::

    $ pip install choicesenum

--------
Features
--------

* An ``ChoicesEnum`` that can be used to create constant groups.
* ``ChoicesEnum`` can define labels to be used in `choices` fields.
* Django fields included:  ``EnumCharField`` and ``EnumIntegerField``.
* All ``ChoicesEnum`` types can be compared against their primitive values directly.
* Support (tested) for Python 2.7, 3.5, 3.6, 3.7 and 3.8.
* Support (tested) for Django 1.9, 1.10, 1.11, 2.0, 2.1, 2.2 and 3.0.

--------------
Usage examples
--------------

Example with ``HttpStatuses``:

.. code:: python

    class HttpStatuses(ChoicesEnum):
        OK = 200
        BAD_REQUEST = 400
        UNAUTHORIZED = 401
        FORBIDDEN = 403

Example with ``Colors``:

.. code:: python

    from choicesenum import ChoicesEnum

    class Colors(ChoicesEnum):
        RED = '#f00', 'Vermelho'
        GREEN = '#0f0', 'Verde'
        BLUE = '#00f', 'Azul'


Comparison
----------

All `Enum` types can be compared against their values:

.. code:: python

    assert HttpStatuses.OK == 200
    assert HttpStatuses.BAD_REQUEST == 400
    assert HttpStatuses.UNAUTHORIZED == 401
    assert HttpStatuses.FORBIDDEN == 403

    status_code = HttpStatuses.OK
    assert 200 <= status_code <= 300

    assert Colors.RED == '#f00'
    assert Colors.GREEN == '#0f0'
    assert Colors.BLUE == '#00f'


Label for free
--------------

All `Enum` types have by default a `display` derived from the enum identifier:

.. code:: python

    assert HttpStatuses.OK.display == 'Ok'
    assert HttpStatuses.BAD_REQUEST.display == 'Bad request'
    assert HttpStatuses.UNAUTHORIZED.display == 'Unauthorized'
    assert HttpStatuses.FORBIDDEN.display == 'Forbidden'


You can easily define your own custom display for an `Enum` item using a tuple:


.. code:: python

    class HttpStatuses(ChoicesEnum):
        OK = 200, 'Everything is fine'
        BAD_REQUEST = 400, 'You did a mistake'
        UNAUTHORIZED = 401, 'I know your IP'
        FORBIDDEN = 403

    assert HttpStatuses.OK.display == 'Everything is fine'
    assert HttpStatuses.BAD_REQUEST.display == 'You did a mistake'
    assert HttpStatuses.UNAUTHORIZED.display == 'I know your IP'
    assert HttpStatuses.FORBIDDEN.display == 'Forbidden'


Dynamic properties
------------------

For each enum item, a dynamic property ``is_<enum_item>`` is generated to allow
quick boolean checks:

.. code:: python

    color = Colors.RED
    assert color.is_red
    assert not color.is_blue
    assert not color.is_green

This feature is usefull to avoid comparing a received enum value against a know enum item.

For example, you can replace code like this:

.. code:: python

    # status = HttpStatuses.BAD_REQUEST

    def check_status(status):
        if status == HttpStatuses.OK:
            print("Ok!")

To this:

.. code:: python

    def check_status(status):
        if status.is_ok:
            print("Ok!")


Custom methods and properties
-----------------------------

You can declare custom properties and methods:

.. code:: python

    class HttpStatuses(ChoicesEnum):
        OK = 200, 'Everything is fine'
        BAD_REQUEST = 400, 'You did a mistake'
        UNAUTHORIZED = 401, 'I know your IP'
        FORBIDDEN = 403

        @property
        def is_error(self):
            return self >= self.BAD_REQUEST

    assert HttpStatuses.OK.is_error is False
    assert HttpStatuses.BAD_REQUEST.is_error is True
    assert HttpStatuses.UNAUTHORIZED.is_error is True

Iteration
---------

The enum type is iterable:

.. code:: python

    >>> for color in Colors:
    ...     print(repr(color))
    Color('#f00').RED
    Color('#0f0').GREEN
    Color('#00f').BLUE


Order is guaranteed only for py3.4+. For fixed order in py2.7, you
can implement a magic attribute ``_order_``:

.. code:: python

    from choicesenum import ChoicesEnum

    class Colors(ChoicesEnum):
        _order_ = 'RED GREEN BLUE'

        RED = '#f00', 'Vermelho'
        GREEN = '#0f0', 'Verde'
        BLUE = '#00f', 'Azul'

Choices
-------

Use ``.choices()`` method to receive a list of tuples ``(item, display)``:

.. code:: python

    assert list(Colors.choices()) == [
        ('#f00', 'Vermelho'),
        ('#0f0', 'Verde'),
        ('#00f', 'Azul'),
    ]

Values
-------

Use ``.values()`` method to receive a list of the inner values:

.. code:: python

    assert Colors.values() == ['#f00', '#0f0', '#00f', ]

Options
-------

Even if a ``ChoicesEnum`` class is an iterator by itself, you can use ``.options()`` to convert the enum items to a list:

.. code:: python

    assert Colors.options() == [Colors.RED, Colors.GREEN, Colors.BLUE]

A "dict like" get
-----------------

Use ``.get(value, default=None)`` method to receive ``default`` if ``value`` is not an item of enum:

.. code:: python

    assert Colors.get(Colors.RED) == Colors.RED
    assert Colors.get('#f00') == Colors.RED
    assert Colors.get('undefined_color') is None
    assert Colors.get('undefined_color', Colors.RED) == Colors.RED

Compatibility
-------------

The enum item can be used whenever the value is needed:

.. code:: python

    assert u'Currrent color is {c} ({c.display})'.format(c=color) ==\
           u'Currrent color is #f00 (Vermelho)'

Even in dicts and sets, as it shares the same `hash()` from his value:

.. code:: python

    d = {
        HttpStatuses.OK.value: "using value",
        HttpStatuses.BAD_REQUEST: "using enum",
        401: "from original value",
    }
    assert d[HttpStatuses.OK] == "using value"
    assert d[HttpStatuses.BAD_REQUEST.value] == "using enum"
    assert d[HttpStatuses.OK] == d[HttpStatuses.OK.value]
    assert d[HttpStatuses.UNAUTHORIZED] == d[401]

There's also optimistic casting of inner types:

.. code:: python

    assert int(HttpStatuses.OK) == 200
    assert float(HttpStatuses.OK) == 200.0
    assert str(HttpStatuses.BAD_REQUEST) == "400"


Check membership:

.. code:: python

    assert HttpStatuses.OK in HttpStatuses
    assert 200 in HttpStatuses
    assert 999 not in HttpStatuses


JSON
....

If you want json serialization, you have at least two options:

1. Patch the default serializer.
2. Write a custom JSONEncoder.

ChoicesEnum comes with a handy patch funtion, you need to add this
code to somewhere at the top of everything to automagically add
json serialization capabilities:

.. code:: python

    from choicesenum.patches import patch_json
    patch_json()

.. note::

    Eventually ``__json__`` will be added to the stdlib, see
    https://bugs.python.org/issue27362


------
Django
------

Fields
------

Usage with the custom Django fields:

.. code:: python

    from django.db import models
    from choicesenum.django.fields import EnumCharField

    class ColorModel(models.Model):
        color = EnumCharField(
            max_length=100,
            enum=Colors,
            default=Colors.GREEN,
        )

    instance = ColorModel()
    assert instance.color ==  Colors.GREEN
    assert instance.color.is_green is True
    assert instance.color.value == Colors.GREEN.value == '#0f0'
    assert instance.color.display == Colors.GREEN.display

    instance.color = '#f00'
    assert instance.color == '#f00'
    assert instance.color.value == '#f00'
    assert instance.color.display == 'Vermelho'


Is guaranteed that the field value is *always* a `ChoicesEnum` item. Pay
attention that the field will only accept valid values for the ``Enum`` in use,
so if your field allow `null`, your enum should also:

.. code:: python

    from django.db import models
    from choicesenum import ChoicesEnum
    from choicesenum.django.fields import EnumIntegerField

    class UserStatus(ChoicesEnum):
        UNDEFINED = None
        PENDING = 1
        ACTIVE = 2
        INACTIVE = 3
        DELETED = 4


    class User(models.Model):
        status = EnumIntegerField(enum=UserStatus, null=True, )

    instance = User()
    assert instance.status.is_undefined is True
    assert instance.status.value is None
    assert instance.status == UserStatus.UNDEFINED
    assert instance.status.display == 'Undefined'

    # again...
    instance.status = None
    assert instance.status.is_undefined is True


--------
Graphene
--------

Usage with Graphene_ Enums:

.. _Graphene: http://docs.graphene-python.org/en/latest/types/enums/#usage-with-python-enums

.. code:: python

    UserStatusEnum = graphene.Enum.from_enum(UserStatus)


----------
Schematics
----------

Usage with Schematics_ Enums:

.. _Schematics: https://schematics.readthedocs.io/en/latest/usage/types.html

.. code:: python

    from schematics.models import Model as SchematicModel
    from schematics.types import StringType, DateTimeType
    from choicesenum import ChoicesEnum
    from choicesenum.schematics.types import ChoicesEnumType

    class HttpStatuses(ChoicesEnum):
        OK = 200
        BAD_REQUEST = 400
        UNAUTHORIZED = 401
        FORBIDDEN = 403

    class CustomSchematicModel(SchematicModel):
        name = StringType(required=True, max_length=255)
        created = DateTimeType(required=True, formats=('%d/%m/%Y', ''))
        http = ChoicesEnumType(HttpStatuses, required=True)
