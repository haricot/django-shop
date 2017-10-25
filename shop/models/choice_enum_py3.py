# -*- coding: utf-8 -*-
from enum import Enum, EnumMeta
from django.utils.six import string_types
from django.utils.translation import ugettext_lazy as _, ugettext


class ChoiceEnumMeta(EnumMeta):
    def __call__(cls, value, *args, **kwargs):
        if isinstance(value, string_types):
            try:
                value = cls.__members__[value]
            except KeyError:
                pass  # let the super method complain
        return super(ChoiceEnumMeta, cls).__call__(value, *args, **kwargs)


class AutoIntEnum(int, Enum, metaclass=ChoiceEnumMeta):
    "base class for name=value int enums"


class ChoiceEnum(AutoIntEnum):
    """
    Utility classe to handle choices in Django model fields
    """
    def __str__(self):
        return ugettext('.'.join((self.__class__.__name__, self.name)))

    @classmethod
    def default(cls):
        try:
            return next(iter(cls))
        except StopIteration:
            return None

    @classmethod
    def choices(cls):
        choices = [(c.value, str(c)) for c in cls]
        return choices
