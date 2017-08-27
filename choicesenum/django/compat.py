# coding: utf-8
from __future__ import absolute_import, unicode_literals


class Creator(object):
    """
    Django 1.10 removed the SubfieldBase. We have backported the to_python
    behaviour for <=1.9 code by copying Creator from Django's 1.8.x branch:
      ``django.db.models.fields.subclassing``
    """
    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:  # pragma: no cover
            return self
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        obj.__dict__[self.field.name] = self.field.to_python(value)
