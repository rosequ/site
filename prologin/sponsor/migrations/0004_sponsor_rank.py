# Generated by Django 2.2.10 on 2020-03-10 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0003_remove_order_and_editions'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='rank',
            field=models.CharField(blank=True, choices=[('gold', 'Gold'), ('silver', 'Silver'), ('bronze', 'Bronze')], max_length=20),
        ),
    ]
