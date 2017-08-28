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


Usage examples
--------------

Example of ``HttpStatuses``:

.. code:: python

    class HttpStatuses(ChoicesEnum):
        OK = 200
        BAD_REQUEST = 400
        UNAUTHORIZED = 401
        FORBIDDEN = 403

    assert HttpStatuses.OK == 200
    assert HttpStatuses.BAD_REQUEST == 400
    assert HttpStatuses.UNAUTHORIZED == 401
    assert HttpStatuses.FORBIDDEN == 403

    assert HttpStatuses.OK.display == 'Ok'
    assert HttpStatuses.BAD_REQUEST.display == 'Bad request'  # <- nice!
    assert HttpStatuses.UNAUTHORIZED.display == 'Unauthorized'
    assert HttpStatuses.FORBIDDEN.display == 'Forbidden'


Example of ``Colors``:

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

    assert Colors.RED == Colors.RED
    assert Colors.GREEN == Colors.GREEN
    assert Colors.BLUE == Colors.BLUE

    assert Colors.RED.display == 'Vermelho'
    assert Colors.GREEN.display == 'Verde'
    assert Colors.BLUE.display == 'Azul'

    # choices
    assert list(Colors.choices()) == [
        ('#f00', 'Vermelho'),
        ('#0f0', 'Verde'),
        ('#00f', 'Azul'),
    ]

    # dynamic `is_<enum_item>` attrs
    assert Colors.RED.is_red
    assert Colors.GREEN.is_green
    assert Colors.BLUE.is_blue

    assert not Colors.RED.is_blue
    assert not Colors.RED.is_green


Using with django fields::

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
    assert instance.color.value == Colors.GREEN.value
    assert instance.color.display == Colors.GREEN.display

    # the field value is allways an ``ChoicesEnum`` item
    instance.color ==  '#f00'
    assert instance.color.display == 'Vermelho'
    assert instance.color.value == '#f00'

    # and still can be used where the value is needed
    assert instance.color == '#f00'
    assert u'Currrent color is {0} ({0.display})'.format(instance.color) ==\
        u'Currrent color is #f00 (Vermelho)'

Pay attention that the field will only accept valid values for the ``Enum``
in use, so if your field allow `null`, your enum should also::


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
