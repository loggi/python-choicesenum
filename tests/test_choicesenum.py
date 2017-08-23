# coding: utf-8
from __future__ import absolute_import, unicode_literals

import pytest
import pickle

from choicesenum import ChoicesEnum


class Colors(ChoicesEnum):
    _order_ = 'RED GREEN BLUE'
    RED = ('#f00', 'Vermelho')
    GREEN = ('#0f0', 'Verde')
    BLUE = ('#00f', 'Azul')


class HttpStatuses(ChoicesEnum):
    OK = 200
    BAD_REQUEST = (400, 'Bad request')
    UNAUTHORIZED = 401
    FORBIDDEN = 403


@pytest.fixture
def colors():
    return Colors


@pytest.fixture
def http_statuses():
    return HttpStatuses


def test_consts_equality(colors):
    assert colors.RED == '#f00'
    assert colors.GREEN == '#0f0'
    assert colors.BLUE == '#00f'

    assert colors.RED == colors.RED
    assert colors.GREEN == colors.GREEN
    assert colors.BLUE == colors.BLUE


def test_consts_display(colors):
    assert colors.RED.display == 'Vermelho'
    assert colors.GREEN.display == 'Verde'
    assert colors.BLUE.display == 'Azul'


def test_get_choices(colors):
    expected = [
        ('#f00', 'Vermelho'),
        ('#0f0', 'Verde'),
        ('#00f', 'Azul'),
    ]

    assert list(colors.choices()) == expected


def test_dynamic_is_attr(colors):
    assert colors.RED.is_red
    assert colors.GREEN.is_green
    assert colors.BLUE.is_blue

    assert not colors.RED.is_blue
    assert not colors.RED.is_green

    assert not colors.GREEN.is_red
    assert not colors.GREEN.is_blue

    assert not colors.BLUE.is_red
    assert not colors.BLUE.is_green


def test_dynamic_is_attr_of_undefined_enums_should_fail(colors):
    with pytest.raises(AttributeError):
        assert colors.RED.is_banana


@pytest.mark.parametrize('attr', ['RED', 'BLUE', 'GREEN', 'is_red', 'is_blue', 'is_green'])
def test_dynamic_is_attr_should_be_in_dir(colors, attr):
        assert attr in dir(colors.RED)


def test_in_format(colors):
    assert '{}'.format(colors.RED) == "#f00"
    assert '{!r}'.format(colors.RED) == "<Colors.RED: '#f00'>"


def test_get_const_by_value(colors):
    assert colors("#f00") == colors.RED
    assert colors("#0f0") == colors.GREEN
    assert colors("#00f") == colors.BLUE

    with pytest.raises(ValueError):
        colors('missing-value')


def test_display_not_defined_should_be_the_name(http_statuses):
    assert http_statuses.OK.display == 'OK'
    assert http_statuses.BAD_REQUEST.display == 'Bad request'
    assert http_statuses.UNAUTHORIZED.display == 'UNAUTHORIZED'
    assert http_statuses.FORBIDDEN.display == 'FORBIDDEN'


def test_consts_equality_for_numbers(http_statuses):
    assert http_statuses.OK == 200
    assert http_statuses.BAD_REQUEST == 400
    assert http_statuses.UNAUTHORIZED == 401
    assert http_statuses.FORBIDDEN == 403

    assert http_statuses.OK == http_statuses.OK


@pytest.mark.parametrize('expected', [Colors.RED, HttpStatuses.UNAUTHORIZED])
def test_enum_should_be_serializable(expected):
    data = pickle.dumps(expected)

    value = pickle.loads(data)
    assert value == expected
    assert value.value == expected.value
