# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-26 21:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=140, verbose_name='Optional name')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('initiator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mailing_batches', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Batch',
                'verbose_name_plural': 'Batches',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='BatchEmail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('state', models.PositiveIntegerField(db_index=True, default=1)),
                ('to', models.EmailField(max_length=254)),
                ('subject', models.TextField(blank=True)),
                ('body', models.TextField(blank=True)),
                ('html_body', models.TextField(blank=True, default="")),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emails', to='mailing.Batch')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['state'],
            },
        ),
        migrations.AlterField(
            model_name='query',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='query',
            name='name',
            field=models.CharField(max_length=144, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='query',
            name='query',
            field=models.TextField(verbose_name='Query'),
        ),
        migrations.AlterField(
            model_name='query',
            name='useful_with',
            field=models.ManyToManyField(blank=True, related_name='useful_queries', to='mailing.Template', verbose_name='Useful with templates'),
        ),
        migrations.AddField(
            model_name='batch',
            name='query',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='batches', to='mailing.Query', verbose_name='Query'),
        ),
        migrations.AddField(
            model_name='batch',
            name='template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='batches', to='mailing.Template', verbose_name='Template'),
        ),
    ]