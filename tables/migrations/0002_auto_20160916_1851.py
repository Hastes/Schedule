# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-16 11:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Fackultet',
            new_name='Faculty',
        ),
        migrations.RenameField(
            model_name='faculty',
            old_name='name_department',
            new_name='name_fac',
        ),
    ]
