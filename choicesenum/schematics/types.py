# coding: utf-8
from __future__ import absolute_import, unicode_literals

from choicesenum import ChoicesEnum
from schematics.types import BaseType
from schematics.exceptions import ValidationError


class ChoicesEnumType(BaseType):
    def __init__(self, type_, **kwargs):
        if not issubclass(type_, ChoicesEnum):
            raise ValidationError(self.Messages.INVALID_TYPE)
        super(ChoicesEnumType, self).__init__(type_, kwargs)
        self.type = type_

    def to_native(self, value, context=None):
        return self.type(value)

    def to_primitive(self, value, context=None):
        return self.type(value).value

    class Messages:
        INVALID_TYPE = 'Expected a ChoicesEnum sub type'
