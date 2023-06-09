# Generated by Django 4.2 on 2023-06-10 19:42

import banking_app.utils
from django.db import migrations, models
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('banking_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_number',
            field=models.CharField(default=functools.partial(banking_app.utils.account_number_generator, *(models.CharField(choices=[('Savings', 'Savings'), ('Current', 'Current')], max_length=16),), **{}), editable=False, unique=True),
        ),
    ]
