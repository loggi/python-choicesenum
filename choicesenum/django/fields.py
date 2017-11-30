# coding: utf-8

from __future__ import absolute_import, unicode_literals

from django.core import checks
from django.db import models
from django.utils.translation import ugettext as _
from django.utils import six
try:
    from django.utils.module_loading import import_string
except ImportError:  # pragma: no cover, Django 1.6 compat
    from django.utils.module_loading import import_by_path as import_string

from .compat import Creator
from ..enums import ChoicesEnum


class FieldErrors(ChoicesEnum):
    E01 = 'choicesenum.E01', _("{cls} has `null=True` but {enum} does not have an item with "
                               "value `None`.")
    E02 = 'choicesenum.E02', _("{cls}: '{default}' is not a valid default for '{enum}'.")


class EnumFieldMixin(object):

    def __init__(self, enum=None, **kwargs):
        choices = kwargs.pop('choices', None)
        if enum and isinstance(enum, six.string_types):
            enum = import_string(enum)

        if choices is None and enum:
            choices = enum.choices()
        kwargs['choices'] = choices
        self.enum = enum
        super(EnumFieldMixin, self).__init__(**kwargs)

    def check(self, **kwargs):
        try:
            errors = super(EnumFieldMixin, self).check(**kwargs)
        except BaseException:
            errors = []
        errors.extend(self._check_null(**kwargs))
        errors.extend(self._check_default(**kwargs))
        return errors

    def _check_null(self, **kwargs):
        if self.null:
            try:
                self.enum(None)
                return []
            except ValueError:
                return [
                    checks.Error(
                        FieldErrors.E01.display.format(
                            cls=self.__class__.__name__, enum=self.enum,),
                        obj=self,
                        id=FieldErrors.E01,
                        hint=_('Add an enum item with `None` as value, eg.: '
                               '`UNDEFINED = None`, or turn `null=False`.'),
                    )
                ]
        return []

    def _check_default(self, **kwargs):
        try:
            default = self.get_default()
            self.enum(default)
            return []
        except ValueError:
            return [
                checks.Error(
                    FieldErrors.E02.display.format(
                        cls=self.__class__.__name__, default=default, enum=self.enum,),
                    obj=self,
                    id=FieldErrors.E02,
                    hint=_('Add an enum item with `{0!r}` as value, eg.: `UNDEFINED = {0!r}`, '
                           'or inform a valid default value.').format(default),
                )
            ]

    def contribute_to_class(self, cls, name):
        # Retain to_python behaviour for < Django 1.8 with removal
        # of SubfieldBase
        super(EnumFieldMixin, self).contribute_to_class(cls, name)
        setattr(cls, name, Creator(self))

    def to_python(self, value):
        return self.enum(value)

    def from_db_value(self, value, expression, connection, context):
        try:
            return self.enum(value)
        except ValueError:
            # We need to return None here even if the enum has no None value
            # to support models being fetched via select_related.
            # The row converters are run before the pk=None check in
            # the default Django model managers.
            if value is None:
                return value
            raise

    def get_prep_value(self, value):
        enum_value = self.to_python(value)
        return getattr(enum_value, 'value', value)

    def deconstruct(self):
        name, path, args, kwargs = super(EnumFieldMixin, self).deconstruct()
        if self.enum:
            kwargs["enum"] = self.enum
            if 'choices' in kwargs:  # pragma: no cover
                del kwargs["choices"]
        return name, path, args, kwargs

    def south_field_triple(self):  # pragma: no cover
        "Returns a suitable description of this field for South (Django 1.6)"
        from south.modelsinspector import introspector
        path = "%s.%s" % (self.__class__.__module__, self.__class__.__name__)
        args, kwargs = introspector(self)
        if 'default' in kwargs and self.default:
            kwargs['default'] = repr(self.to_python(self.default).value)
        if self.enum:
            kwargs['enum'] = repr(self.enum._import_path())
        return (str(path), args, kwargs)


def get_base_classes(cls_type):  # pragma: no cover, already covered by tox matrix
    if hasattr(models, 'SubfieldBase'):
        from django.utils import six
        return six.with_metaclass(models.SubfieldBase, EnumFieldMixin, cls_type)
    else:
        class EnumFieldBase(EnumFieldMixin, cls_type):
            pass
        return EnumFieldBase


class EnumCharField(get_base_classes(models.CharField)):
    description = "A string enum field"


class EnumIntegerField(get_base_classes(models.IntegerField)):
    description = "An integer enum field"
