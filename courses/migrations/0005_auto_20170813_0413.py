# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-13 01:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20170813_0406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentlesson',
            name='mark',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F')], max_length=1),
        ),
    ]
