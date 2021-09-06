# Generated by Django 3.0.3 on 2021-09-06 19:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('access_control', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DGitBlob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Public identifier')),
                ('name', models.TextField()),
                ('path', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('checksum', models.CharField(max_length=20)),
                ('save_path', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dgit_dgitblob_created', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DGitBranch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Public identifier')),
                ('name', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dgit_dgitbranch_created', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dgit_dgitbranch_created', to='dgit.DGitBranch')),
            ],
        ),
        migrations.CreateModel(
            name='DGitCommit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Public identifier')),
                ('message', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('blobs', models.ManyToManyField(to='dgit.DGitBlob')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dgit_dgitcommit_branch', to='dgit.DGitBranch')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dgit_dgitcommit_owner', to=settings.AUTH_USER_MODEL)),
                ('prev_commit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dgit_dgitcommit_prev_commit', to='dgit.DGitCommit')),
            ],
        ),
        migrations.CreateModel(
            name='DGitRepository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Public identifier')),
                ('name', models.TextField()),
                ('visibilty', models.BooleanField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dgit_dgitrepository_created', to=settings.AUTH_USER_MODEL)),
                ('policy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dgit_dgitrepository_created', to='access_control.Policy')),
            ],
        ),
        migrations.CreateModel(
            name='DGitPush',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Public identifier')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('commit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dgit_dgitpush_commit', to='dgit.DGitCommit')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dgit_dgitpush_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DGitFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Public identifier')),
                ('name', models.CharField(max_length=100)),
                ('path', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now_add=True)),
                ('commit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dgit_dgitfile_commit', to='dgit.DGitCommit')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dgit_dgitfile_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='dgitbranch',
            name='repository',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dgit_dgitbranch_created', to='dgit.DGitRepository'),
        ),
    ]
