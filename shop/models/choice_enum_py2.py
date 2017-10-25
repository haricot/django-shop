# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from enum import Enum, EnumMeta

from django.utils.six import python_2_unicode_compatible, with_metaclass, string_types
from django.utils.translation import ugettext_lazy as _, ugettext


class ChoiceEnumMeta(EnumMeta):
    def __call__(cls, value, *args, **kwargs):
        if isinstance(value, string_types):
            try:
                value = cls.__members__[value]
            except KeyError:
                pass  # let the super method complain
        return super(ChoiceEnumMeta, cls).__call__(value, *args, **kwargs)


@python_2_unicode_compatible
class ChoiceEnum(with_metaclass(ChoiceEnumMeta, Enum)):
    """
    Utility class to handle choices in Django model fields
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
