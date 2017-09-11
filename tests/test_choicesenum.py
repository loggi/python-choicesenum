# coding: utf-8
from __future__ import absolute_import, unicode_literals

import sys
import operator

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


def test_consts_display_alias_to_description(colors):
    assert colors.RED.display == colors.RED.description == 'Vermelho'


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


def test_values(colors):
    expected = ['#f00', '#0f0', '#00f', ]
    assert sorted(colors.values()) == sorted(expected)


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


def test_should_proxy_len_calls(colors):
    assert len(colors.RED) == len(colors.RED.value) == len('#f00') == 4


def test_should_return_1_when_proxy_len_calls_fail(http_statuses):
    assert len(http_statuses.OK) == len(http_statuses.BAD_REQUEST) == 1


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


def test_enum_should_be_hashable():
    from choicesenum import ChoicesEnum

    class Baz(ChoicesEnum):
        A = 1
        B = 2
        C = 3

    d = {Baz.A: 'foo', Baz.B: 'bar'}

    assert hash(Baz.A) != hash(Baz.B)
    assert set(Baz) == set(Baz)
    assert d[Baz.B] == 'bar'


def test_enum_should_be_sortable():
    from choicesenum import ChoicesEnum

    class Baz(ChoicesEnum):
        A = 3
        B = 5
        C = 1

    assert sorted(Baz) == [Baz.C, Baz.A, Baz.B]


@pytest.mark.parametrize('enum_fixture, left, operator_name, right, expected', [
    # lt
    ('http_statuses', 'BAD_REQUEST', '<', 'UNAUTHORIZED', True),
    ('http_statuses', 'BAD_REQUEST', '<', 400, False),
    ('colors', 'GREEN', '<', 'RED', True),
    ('colors', 'GREEN', '<', '#f00', True),
    # le
    ('http_statuses', 'BAD_REQUEST', '<=', 'UNAUTHORIZED', True),
    ('http_statuses', 'BAD_REQUEST', '<=', 'BAD_REQUEST', True),
    ('http_statuses', 'BAD_REQUEST', '<=', 400, True),
    ('http_statuses', 400, '<=', 'BAD_REQUEST', True),
    ('http_statuses', 'BAD_REQUEST', '<=', 399, False),
    # eq
    ('http_statuses', 'UNAUTHORIZED', '==', 'UNAUTHORIZED', True),
    ('http_statuses', 'UNAUTHORIZED', '==', 401, True),
    ('http_statuses', 'OK', '==', 201, False),
    ('http_statuses', 401, '==', 'UNAUTHORIZED', True),
    # ne
    ('http_statuses', 'UNAUTHORIZED', '!=', 400, True),
    ('http_statuses', 'UNAUTHORIZED', '!=', 'BAD_REQUEST', True),
    # gt
    ('http_statuses', 'UNAUTHORIZED', '>', 'BAD_REQUEST', True),
    ('http_statuses', 'FORBIDDEN', '>', 'UNAUTHORIZED', True),
    ('http_statuses', 'FORBIDDEN', '>', 401, True),
    ('http_statuses', 'FORBIDDEN', '>', 404, False),
    ('http_statuses', 404, '>', 'FORBIDDEN', True),
    # ge
    ('http_statuses', 'UNAUTHORIZED', '>=', 400, True),
    ('http_statuses', 'UNAUTHORIZED', '>=', 401, True),
    ('http_statuses', 401, '>=', 'UNAUTHORIZED', True),
    ('http_statuses', 402, '>=', 'UNAUTHORIZED', True),
])
def test_enum_should_be_comparable(request, enum_fixture, left, operator_name, right, expected):
    enum = request.getfixturevalue(enum_fixture)
    left_item = getattr(enum, str(left), left)
    right_item = getattr(enum, str(right), right)

    operators = {
        '==': operator.eq,
        '!=': operator.ne,
        '>': operator.gt,
        '>=': operator.ge,
        '<': operator.lt,
        '<=': operator.le,
    }
    op = operators[operator_name]

    assert op(left_item, right_item) == expected


def test_integer_enum_should_be_comparable(http_statuses):
    assert 200 <= http_statuses.OK <= 300


@pytest.mark.skipif(
    sys.version_info[:2] == (3, 4),
    reason="Python 3.4 implementation don't allow custom properties"
)
@pytest.mark.parametrize('enum_fixture, attr, property, expected', [
    ('http_statuses', 'OK', 'is_error', False),
    ('http_statuses', 'BAD_REQUEST', 'is_error', True),
])
def test_custom_properties(request, enum_fixture, attr, property, expected):
    enum = request.getfixturevalue(enum_fixture)
    enum_item = getattr(enum, attr)
    prop_value = getattr(enum_item, property)

    assert prop_value == expected
