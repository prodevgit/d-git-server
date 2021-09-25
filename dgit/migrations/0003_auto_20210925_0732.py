# Generated by Django 3.0.3 on 2021-09-25 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dgit', '0002_historicaldgitbranch_historicaldgitrepository'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dgitcommit',
            name='prev_commit',
            field=models.ForeignKey(blank=True, default=True, on_delete=django.db.models.deletion.CASCADE, related_name='dgit_dgitcommit_prev_commit', to='dgit.DGitCommit'),
        ),
    ]
