# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-03 02:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ctflex', '0008_auto_20160402_2204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ctfproblem',
            old_name='description',
            new_name='description_raw',
        ),
        migrations.RenameField(
            model_name='ctfproblem',
            old_name='hint',
            new_name='hint_raw',
        ),
    ]
