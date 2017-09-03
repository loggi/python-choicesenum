# coding: utf-8
from __future__ import absolute_import, unicode_literals

from choicesenum import ChoicesEnum


def format_pytest_id(instance):
    return "%s.%s" % (instance.__class__.__name__, instance._name_,)


def pytest_make_parametrize_id(config, val, argname):
    if isinstance(val, ChoicesEnum):
        return format_pytest_id(val)
