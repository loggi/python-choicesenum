# coding: utf-8
from __future__ import absolute_import, unicode_literals

from django.db import models
from choicesenum.django.fields import EnumCharField, EnumIntegerField

from .enums import Color, UserStatus


class ColorModel(models.Model):
    color = EnumCharField(
        max_length=100,
        enum=Color,
        default=Color.GREEN,
    )


class User(models.Model):
    username = models.CharField(max_length=50)
    status = EnumIntegerField(enum=UserStatus, null=True)


class Preference(models.Model):
    color = models.ForeignKey(ColorModel, null=True)
