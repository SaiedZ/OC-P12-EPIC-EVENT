# Generated by Django 3.2 on 2022-05-19 13:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_auto_20220511_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crmuser',
            name='mobile',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='mobile number'),
        ),
        migrations.AlterField(
            model_name='crmuser',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='phone number'),
        ),
    ]
