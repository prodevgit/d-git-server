# Generated by Django 3.0.3 on 2021-09-07 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dgit', '0002_dgitbranch_merge_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='dgitbranch',
            name='is_root',
            field=models.BooleanField(default=False),
        ),
    ]
