============
Choices Enum
============


.. image:: https://img.shields.io/pypi/v/python-choicesenum.svg
        :target: https://pypi.python.org/pypi/python-choicesenum

.. image:: https://img.shields.io/travis/loggi/python-choicesenum.svg
        :target: https://travis-ci.org/loggi/python-choicesenum

.. image:: https://readthedocs.org/projects/python-choicesenum/badge/?version=latest
        :target: https://python-choicesenum.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/loggi/python-choicesenum/shield.svg
     :target: https://pyup.io/repos/github/loggi/python-choicesenum/
     :alt: Updates


Python's Enum with extra powers to play nice with labels and choices fields.

Work in progress.

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

Usage examples
--------------

Example of ``Colors``:

.. code:: python

    from choicesenum import ChoicesEnum

    class Colors(ChoicesEnum):
        # For fixed order in  py2.7, py3.4+ are ordered by default
        _order_ = 'RED GREEN BLUE'
        RED = ('#f00', 'Vermelho')
        GREEN = ('#0f0', 'Verde')
        BLUE = ('#00f', 'Azul')

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


Example of ``HttpStatuses``:

.. code:: python

    class HttpStatuses(ChoicesEnum):
        OK = 200
        BAD_REQUEST = (400, 'Bad request')
        UNAUTHORIZED = 401
        FORBIDDEN = 403

    assert HttpStatuses.OK == 200
    assert HttpStatuses.BAD_REQUEST == 400
    assert HttpStatuses.UNAUTHORIZED == 401
    assert HttpStatuses.FORBIDDEN == 403

    assert HttpStatuses.OK.display == 'OK'
    assert HttpStatuses.BAD_REQUEST.display == 'Bad request'  # <- nice!
    assert HttpStatuses.UNAUTHORIZED.display == 'UNAUTHORIZED'
    assert HttpStatuses.FORBIDDEN.display == 'FORBIDDEN'
