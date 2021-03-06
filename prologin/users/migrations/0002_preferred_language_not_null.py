# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 01:51
from __future__ import unicode_literals

from django.db import migrations
import prologin.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prologinuser',
            name='preferred_language',
            field=prologin.models.CodingLanguageField(blank=True, choices=[('ada', 'Ada'), ('brainfuck', 'Brainfuck'), ('c', 'C'), ('csharp', 'C#'), ('cpp', 'C++'), ('fsharp', 'F#'), ('haskell', 'Haskell'), ('java', 'Java'), ('js', 'Javascript'), ('lua', 'Lua'), ('ocaml', 'OCaml'), ('pascal', 'Pascal'), ('perl', 'Perl'), ('php', 'PHP'), ('pseudocode', 'Pseudocode'), ('python2', 'Python 2'), ('python3', 'Python 3'), ('scheme', 'Scheme'), ('vb', 'Visual Basic')], db_index=True, default='', max_length=64, verbose_name='Preferred coding language'),
            preserve_default=False,
        ),
    ]
