# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-13 23:06
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20170814_0139'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentlesson',
            name='mark_testing',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='studentlesson',
            name='mark',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F')], max_length=1, null=True),
        ),
    ]
