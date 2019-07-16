# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import PositiveIntegerField
from django.utils.translation import ugettext as _, pgettext
from shop.models import order


class OrderItem(order.BaseOrderItem):
    """Default materialized model for OrderItem"""
    quantity = PositiveIntegerField(_("Ordered quantity"))

    class Meta:
        verbose_name = pgettext('order_models', "Ordered Item")
        verbose_name_plural = pgettext('order_models', "Ordered Items")
