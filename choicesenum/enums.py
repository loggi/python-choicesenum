# coding: utf-8
from __future__ import absolute_import, unicode_literals

from enum import Enum


class ChoicesEnum(Enum):

    def __new__(cls, value, display=None):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._display_ = display
        return obj

    def __getattr__(self, item):
        is_attr = 'is_'
        if item.startswith(is_attr) and item in self._get_dynamic_property_names():
            search = item[len(is_attr):]
            return search == self._name_.lower()
        raise AttributeError("'{}' object has no attribute '{}'".format(type(self).__name__, item))

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "%s(%r).%s" % (self.__class__.__name__, self._value_, self._name_, )

    @staticmethod
    def _get_value(item):
        return getattr(item, 'value', item)

    def __len__(self):
        try:
            return len(self.value)
        except Exception:
            return 1

    def __hash__(self):
        return hash(self._name_)

    def __lt__(self, other):
        return self.value < self._get_value(other)

    def __le__(self, other):
        return self.value <= self._get_value(other)

    def __eq__(self, other):
        return self.value == self._get_value(other)

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return self.value > self._get_value(other)

    def __ge__(self, other):
        return self.value >= self._get_value(other)

    def __dir__(self):
        return sorted(set(
            dir(type(self)) +
            list(self.__dict__.keys()) +
            ['display', 'get_choices', ] +
            list(self._get_dynamic_property_names())
        ))

    @property
    def display(self):
        return self._display_ if self._display_ is not None else\
            self._name_.replace('_', ' ').capitalize()

    @property
    def description(self):
        """
        Alias for `label`, allow enum descriptors to be used by Graphene.
        See: http://docs.graphene-python.org/en/latest/types/enums/#usage-with-python-enums
        """
        return self.display

    @classmethod
    def _get_dynamic_property_names(cls):
        """
        Args:
            cls (Enum): Enum class.
        """
        return ('is_{}'.format(x._name_.lower()) for x in cls)

    @classmethod
    def choices(cls):
        """
        Args:
            cls (Enum): Enum class.
        """
        return [(x, x.display) for x in cls]

    @classmethod
    def values(cls):
        """
        Args:
            cls (Enum): Enum class.
        """
        return [x.value for x in cls]

    @classmethod
    def options(cls):
        """
        Converts the enum options to a list.

        Args:
            cls (Enum): Enum class.
        """
        return list(cls)

    @classmethod
    def _import_path(cls):
        return '{}.{}'.format(cls.__module__, cls.__name__)
