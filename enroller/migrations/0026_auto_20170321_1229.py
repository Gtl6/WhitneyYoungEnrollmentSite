# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-03-21 17:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enroller', '0025_auto_20170320_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainsurvey',
            name='birthDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]