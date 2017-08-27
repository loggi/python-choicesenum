# coding: utf-8
from __future__ import absolute_import, unicode_literals

from django.db import models
from choicesenum.django.fields import EnumCharField

from .enums import Color


class ColorModel(models.Model):
    color = EnumCharField(
        max_length=100,
        enum=Color,
        default=Color.GREEN,
    )
