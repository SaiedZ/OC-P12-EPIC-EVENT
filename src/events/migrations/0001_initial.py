# Generated by Django 3.2 on 2022-05-17 08:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200,
                 unique=True, verbose_name='Event statut')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('attendees', models.IntegerField(blank=True, null=True)),
                ('event_date', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('contract', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,
                 related_name='contract', to='contracts.contract')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                 related_name='event_statut', to='events.eventstatus')),
                ('support_contact', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                 related_name='support_contact', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
