# coding: utf-8

import pytest
from enum import Enum
from choicesenum import ChoicesEnum


class Color(ChoicesEnum):
    RED = '#f00', 'Vermelho'
    GREEN = '#0f0', 'Verde'
    BLUE = '#00f', 'Azul'


class ColorBasicEnum(Enum):
    RED = '#f00'
    GREEN = '#0f0'
    BLUE = '#00f'


class UserStatus(ChoicesEnum):
    UNDEFINED = None
    PENDING = 1
    ACTIVE = 2
    INACTIVE = 3
    DELETED = 4


def test_param_repr():
    from _pytest.python import idmaker

    result = idmaker(("a", "b"), [pytest.param(Color.RED, UserStatus.ACTIVE)])
    assert result == ["Color.RED-UserStatus.ACTIVE"]


def test_param_repr_basic_enum():
    from _pytest.python import idmaker

    result = idmaker(("a", "b"), [
        pytest.param(ColorBasicEnum.RED, ColorBasicEnum.BLUE)])
    assert result == ["ColorBasicEnum.RED-ColorBasicEnum.BLUE"]
