# Generated by Django 3.2 on 2022-05-30 16:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_auto_20220519_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=200, unique=True, validators=[django.core.validators.MinLengthValidator(2)], verbose_name='Team name'),
        ),
    ]
