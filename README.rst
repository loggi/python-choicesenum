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


Python's Enum with extra powers to play nice with labels and choices fields.

* Free software: BSD license
* Documentation: https://python-choicesenum.readthedocs.io.

Installation
------------

Install ``choicesenum`` using pip::

    $ pip install choicesenum


Features
--------

* An ``ChoicesEnum`` that can be used to create constant groups.
* ``ChoicesEnum`` can define labels to be used in `choices` fields.
* Django fields included:  ``EnumCharField`` and ``EnumIntegerField``.
* Support (tested) for Python 2.7, 3.4, 3.5 and 3.6.
* Support (tested) for Django 1.6.1 (with south), 1.7, 1.8, 1.9, 1.10, 1.11 and 2.0.

Usage examples
--------------

Example with ``HttpStatuses``:

.. code:: python

    class HttpStatuses(ChoicesEnum):
        OK = 200
        BAD_REQUEST = 400
        UNAUTHORIZED = 401
        FORBIDDEN = 403

All `Enum` types can be compared against their values:

.. code:: python

    assert HttpStatuses.OK == 200
    assert HttpStatuses.BAD_REQUEST == 400
    assert HttpStatuses.UNAUTHORIZED == 401
    assert HttpStatuses.FORBIDDEN == 403

    status_code = HttpStatuses.OK
    assert 200 <= status_code <= 300


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


Example with ``Colors``:

.. code:: python

    from choicesenum import ChoicesEnum

    class Colors(ChoicesEnum):
        # For fixed order in  py2.7, py3.4+ are ordered by default
        _order_ = 'RED GREEN BLUE'

        RED = '#f00', 'Vermelho'
        GREEN = '#0f0', 'Verde'
        BLUE = '#00f', 'Azul'

    assert Colors.RED == '#f00'
    assert Colors.GREEN == '#0f0'
    assert Colors.BLUE == '#00f'

    assert Colors.RED.display == 'Vermelho'
    assert Colors.GREEN.display == 'Verde'
    assert Colors.BLUE.display == 'Azul'


Use ``.choices()`` method to receive a list of tuples ``(item, display)``:

.. code:: python

    # choices
    assert list(Colors.choices()) == [
        ('#f00', 'Vermelho'),
        ('#0f0', 'Verde'),
        ('#00f', 'Azul'),
    ]


For each enum item, a dynamic property ``is_<enum_item>`` is generated to allow
quick boolean checks:

.. code:: python

    color = Colors.RED
    assert color.is_red
    assert not color.is_blue
    assert not color.is_green

    if color.is_red:
        print 'Is red!'

The enum item can be used whenever the value is needed:

.. code:: python

    assert u'Currrent color is {c} ({c.display})'.format(c=color) ==\
           u'Currrent color is #f00 (Vermelho)'

Even in dicts and sets, as it shares the same `hash()` from his value:

.. code:: python

    d = {
        HttpStatuses.OK.value: "nice",
        HttpStatuses.BAD_REQUEST.value: "bad",
        401: "Don't do this",
    }
    assert d[HttpStatuses.OK] == "nice"
    assert d[HttpStatuses.OK.value] == "nice"
    assert d[HttpStatuses.OK] == d[HttpStatuses.OK.value]
    assert d[HttpStatuses.UNAUTHORIZED] == d[401]


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

Usage with Graphene_ Enums:

.. _Graphene: http://docs.graphene-python.org/en/latest/types/enums/#usage-with-python-enums

.. code:: python

    UserStatusEnum = graphene.Enum.from_enum(UserStatus)
