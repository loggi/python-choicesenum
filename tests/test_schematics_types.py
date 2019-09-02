# coding: utf-8
from __future__ import absolute_import, unicode_literals

import pytest
from schematics.exceptions import ValidationError
from choicesenum.schematics.types import ChoicesEnumType


def test_choices_enum_type(http_statuses):
    state = ChoicesEnumType(http_statuses)
    assert state.to_native(200) is http_statuses.OK
    assert state.to_primitive(200) == http_statuses.OK.value


def test_choices_enum_type_with_extra_params(http_statuses):
    state = ChoicesEnumType(http_statuses, required=True)
    assert state.to_native(200) is http_statuses.OK


def test_choices_enum_type_should_throw_exception():
    with pytest.raises(ValidationError) as e:
        ChoicesEnumType(object)
        assert e.value.message[0] == ChoicesEnumType.Messages.INVALID_TYPE
