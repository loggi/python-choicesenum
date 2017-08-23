============
Choices Enum
============


.. image:: https://img.shields.io/pypi/v/choicesenum.svg
        :target: https://pypi.python.org/pypi/choicesenum

.. image:: https://img.shields.io/travis/loggi/choicesenum.svg
        :target: https://travis-ci.org/loggi/choicesenum

.. image:: https://readthedocs.org/projects/choicesenum/badge/?version=latest
        :target: https://choicesenum.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/loggi/choicesenum/shield.svg
     :target: https://pyup.io/repos/github/loggi/choicesenum/
     :alt: Updates


Python's Enum with extra powers to play nice with labels and choices fields.

Work in progress.

* Free software: BSD license
* Documentation: https://choicesenum.readthedocs.io.

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

    assert colors.RED == '#f00'
    assert colors.GREEN == '#0f0'
    assert colors.BLUE == '#00f'

    assert colors.RED == colors.RED
    assert colors.GREEN == colors.GREEN
    assert colors.BLUE == colors.BLUE

    assert colors.RED.display == 'Vermelho'
    assert colors.GREEN.display == 'Verde'
    assert colors.BLUE.display == 'Azul'

    # choices
    assert list(colors.choices()) == [
        ('#f00', 'Vermelho'),
        ('#0f0', 'Verde'),
        ('#00f', 'Azul'),
    ]

    # dynamic `is_<enum_item>` attrs
    assert colors.RED.is_red
    assert colors.GREEN.is_green
    assert colors.BLUE.is_blue

    assert not colors.RED.is_blue
    assert not colors.RED.is_green


Example of ``HttpStatuses``:

.. code:: python

    class HttpStatuses(ChoicesEnum):
        OK = 200
        BAD_REQUEST = (400, 'Bad request')
        UNAUTHORIZED = 401
        FORBIDDEN = 403

    assert http_statuses.OK == 200
    assert http_statuses.BAD_REQUEST == 400
    assert http_statuses.UNAUTHORIZED == 401
    assert http_statuses.FORBIDDEN == 403

    assert http_statuses.OK.display == 'OK'
    assert http_statuses.BAD_REQUEST.display == 'Bad request'  # <- nice!
    assert http_statuses.UNAUTHORIZED.display == 'UNAUTHORIZED'
    assert http_statuses.FORBIDDEN.display == 'FORBIDDEN'
