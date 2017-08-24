# coding: utf-8

from __future__ import absolute_import, unicode_literals

import six
from django.db import models


class ChoicesEnumFieldMixin(object):
    description = "A const field"

    def __init__(self, choices_enum_class=None, *args, **kwargs):
        choices = kwargs.pop('choices', None)
        if choices is None and choices_enum_class:
            choices = choices_enum_class.get_choices()
        kwargs['choices'] = choices
        super(ChoicesEnumStringField, self).__init__(*args, **kwargs)
        self.choices_enum_class = choices_enum_class

    def to_python(self, value):
        return self.choices_enum_class(value)

    def get_prep_value(self, value):
        return getattr(value, 'value', value)


class ChoicesEnumStringField(
        six.with_metaclass(models.SubfieldBase, ChoicesEnumFieldMixin, models.CharField)):
    description = "A string const field"


class ChoicesEnumIntegerField(
        six.with_metaclass(models.SubfieldBase, ChoicesEnumFieldMixin, models.IntegerField)):
    description = "An integer const field"


try:
    # if south is installed, be nice and let it know that it has the same
    # introspection rules as its base class
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules(
        [], ["^choicesenum\.django\.fields\.ChoicesEnumStringField"])
    add_introspection_rules(
        [], ["^choicesenum\.django\.fields\.ChoicesEnumIntegerField"])
except ImportError:
    pass
