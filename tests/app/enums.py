# coding: utf-8
from __future__ import absolute_import, unicode_literals

from choicesenum import ChoicesEnum


class Color(ChoicesEnum):
    RED = '#f00', 'Vermelho'
    GREEN = '#0f0', 'Verde'
    BLUE = '#00f', 'Azul'


class UserStatus(ChoicesEnum):
    UNDEFINED = None
    PENDING = 1
    ACTIVE = 2
    INACTIVE = 3
    DELETED = 4


class HttpStatus(ChoicesEnum):
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403

    @property
    def is_error(self):
        return self >= self.BAD_REQUEST


class Sizes(ChoicesEnum):
    EMPTY = None
    NOT_INFORMED = ''
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'
