# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-15 01:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_auto_20170815_0252'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentlesson',
            old_name='reason_for_precense',
            new_name='reason_for_abcense',
        ),
    ]
