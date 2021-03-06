# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-30 22:25
from __future__ import unicode_literals

from django.db import migrations
import prologin.models
import team.models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0003_member_role_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teammember',
            name='role',
        ),
        migrations.DeleteModel(
            name='Role',
        ),
        migrations.AlterField(
            model_name='teammember',
            name='role_code',
            field=prologin.models.TextEnumField(team.models.Role, choices=[('president', 'President'), ('vice_president', 'Vice President'), ('treasurer', 'Treasurer'), ('secretary', 'Secretary'), ('technical_lead', 'Technical Lead'), ('scientific_lead', 'Scientific Lead'), ('vice_treasurer', 'Vice Treasurer'), ('member', 'Member'), ('persistent_member', 'Persistent Member'), ('mascot', 'Mascot'), ('external_organizer', 'External organizer')], db_index=True, max_length=64, verbose_name='Role'),
        ),
    ]
