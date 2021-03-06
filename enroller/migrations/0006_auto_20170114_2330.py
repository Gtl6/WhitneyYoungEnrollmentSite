# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-15 05:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enroller', '0005_auto_20170111_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='emergencyandhealthinfo',
            name='doctorAddress',
            field=models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.CASCADE, to='enroller.Address'),
        ),
        migrations.AddField(
            model_name='guardian',
            name='homeAddress',
            field=models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.CASCADE, related_name='homeAddress', to='enroller.Address'),
        ),
        migrations.AddField(
            model_name='guardian',
            name='workAddress',
            field=models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.CASCADE, related_name='workAddress', to='enroller.Address'),
        ),
    ]
