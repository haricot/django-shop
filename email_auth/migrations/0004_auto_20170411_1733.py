# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-11 15:33
from __future__ import unicode_literals

from django import VERSION

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_auth', '0003_django110'),
    ]

    operations = []

    if VERSION >= (1, 10):
        from django.contrib.auth import validators
        from django.utils import six

        operations.append(
            migrations.AlterField(
                model_name='user',
                name='last_name',
                field=models.CharField(
                    error_messages={'unique': 'A user with that username already exists.'},
                    help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                    max_length=150,
                    unique=True,
                    validators=[validators.UnicodeUsernameValidator() if six.PY3 else validators.ASCIIUsernameValidator()],
                    verbose_name='last_name'),
            )
        )
