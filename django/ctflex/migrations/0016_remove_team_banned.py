# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-03 23:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ctflex', '0015_team_banned_standing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='banned',
        ),
    ]