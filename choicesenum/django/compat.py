# coding: utf-8
from __future__ import absolute_import, unicode_literals

import django
from django.db.models.query_utils import DeferredAttribute


class Creator(DeferredAttribute):
    """
    Django 1.10 removed the SubfieldBase. We have backported the to_python
    behaviour for <=1.9 code by copying Creator from Django's 1.8.x branch:
      ``django.db.models.fields.subclassing``
    """
    def __init__(self, field, model):
        self.field = field
        if django.VERSION < (2, 1):  # pragma: no cover (Django < 2.1 compat)
            super(Creator, self).__init__(field.attname, model)
        elif django.VERSION < (3, 0):  # pragma: no cover (Django < 3.0 compat)
            super(Creator, self).__init__(field.attname)
        else:  # pragma: no cover
            super(Creator, self).__init__(field)

    def __set__(self, obj, value):
        field_name = getattr(self, 'field_name', self.field.attname)
        obj.__dict__[field_name] = self.field.to_python(value)
