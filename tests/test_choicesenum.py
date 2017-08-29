# coding: utf-8
from __future__ import absolute_import, unicode_literals

import sys
import pytest
import pickle


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

    assert sorted(colors.choices(), key=lambda c: c[0].value) == sorted(expected)


def test_options(colors):
    expected = ['#f00', '#0f0', '#00f', ]
    assert sorted(colors.options(), key=lambda c: c.value) == sorted(expected)


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


@pytest.mark.skipif(sys.version_info < (3, 0), reason="requires python3")
def test_in_format_python3(colors):
    assert '{}'.format(colors.RED) == "#f00"
    assert '{!r}'.format(colors.RED) == "Color('#f00').RED"


@pytest.mark.skipif(sys.version_info >= (3, 0), reason="requires python2")
def test_in_format_python2(colors):
    assert '{}'.format(colors.RED) == "#f00"
    assert '{!r}'.format(colors.RED) == "Color(u'#f00').RED"


@pytest.mark.skipif(
    sys.version_info[:2] == (3, 4),
    reason="Python 3.4 implementation don't allow access item from a item, eg. Color.RED.GREEN"
)
def test_should_reconstruct_instance_from_repr():
    from tests.app.enums import Color
    red_repr = repr(Color.RED)
    print(red_repr)
    red_from_repr = eval(red_repr)
    assert red_from_repr is Color.RED
    assert red_from_repr == Color.RED


def test_get_const_by_value(colors):
    assert colors("#f00") == colors.RED
    assert colors("#0f0") == colors.GREEN
    assert colors("#00f") == colors.BLUE

    with pytest.raises(ValueError):
        colors('missing-value')


@pytest.mark.parametrize('enum_fixture, attr, display', [
    ('colors', 'RED', 'Vermelho', ),
    ('http_statuses', 'OK', 'Ok', ),
    ('http_statuses', 'BAD_REQUEST', 'Bad request', ),
    ('http_statuses', 'UNAUTHORIZED', 'Unauthorized', ),
    ('http_statuses', 'FORBIDDEN', 'Forbidden', ),
])
def test_display_not_defined_should_be_the_name(
        request, enum_fixture, attr, display):
    enum = request.getfixturevalue(enum_fixture)
    enum = getattr(enum, attr)
    assert enum.display == display


def test_consts_equality_for_numbers(http_statuses):
    assert http_statuses.OK == 200
    assert http_statuses.BAD_REQUEST == 400
    assert http_statuses.UNAUTHORIZED == 401
    assert http_statuses.FORBIDDEN == 403

    assert http_statuses.OK == http_statuses.OK


@pytest.mark.parametrize('expected', ['colors', 'http_statuses'])
def test_enum_should_be_serializable(request, expected):
    choicesenum = request.getfixturevalue(expected)
    for item in choicesenum:
        data = pickle.dumps(item)

        value = pickle.loads(data)
        assert value == item
        assert value.value == item.value
