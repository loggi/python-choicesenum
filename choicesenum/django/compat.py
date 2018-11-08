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
    if django.VERSION < (2, 1):
        def __init__(self, field, model):
            self.field = field
            super(Creator, self).__init__(field.attname, model)

    else:
        def __init__(self, field, model):
            self.field = field
            super(Creator, self).__init__(field.attname)

    def __set__(self, obj, value):
        obj.__dict__[self.field_name] = self.field.to_python(value)
