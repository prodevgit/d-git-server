# Generated by Django 3.0.3 on 2021-09-05 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('access_control', '0002_auto_20210905_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='policy',
            name='name',
        ),
    ]
