# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-03-07 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enroller', '0018_simplefile'),
    ]

    operations = [
        migrations.AddField(
            model_name='simplefile',
            name='uploadHistory',
            field=models.DateField(default='1998-11-26'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='divisionNumber',
            field=models.CharField(max_length=4),
        ),
    ]
