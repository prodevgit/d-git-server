import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from access_control.models import Policy


class DGitFile(models.Model):
    object_id = models.UUIDField(unique=True, editable=False,
                                 default=uuid.uuid4, verbose_name='Public identifier')
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                      related_name="%(app_label)s_%(class)s_owner")
    path = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    last_update = models.DateTimeField(auto_now_add=True, blank=True)
    commit = models.ForeignKey('DGitCommit', related_name='%(app_label)s_%(class)s_commit',
                                    db_index=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class DGitPush(models.Model):
    object_id = models.UUIDField(unique=True, editable=False,
                                 default=uuid.uuid4, verbose_name='Public identifier')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name="%(app_label)s_%(class)s_owner")
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    commit = models.ForeignKey('DGitCommit', related_name='%(app_label)s_%(class)s_commit',
                               db_index=True, on_delete=models.CASCADE)

class DGitCommit(models.Model):
    object_id = models.UUIDField(unique=True, editable=False,
                                 default=uuid.uuid4, verbose_name='Public identifier')
    message = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name="%(app_label)s_%(class)s_owner")
    created = models.DateTimeField(auto_now_add=True, blank=True)
    branch =  models.ForeignKey('DGitBranch', related_name='%(app_label)s_%(class)s_branch',
                                    db_index=True, on_delete=models.CASCADE)
    blobs = models.ManyToManyField('DGitBlob')
    prev_commit = models.ForeignKey('DGitCommit', related_name='%(app_label)s_%(class)s_prev_commit',
                                    db_index=True, on_delete=models.CASCADE)

class DGitBranch(models.Model):
    object_id = models.UUIDField(unique=True, editable=False,
                                 default=uuid.uuid4, verbose_name='Public identifier')
    parent =  models.ForeignKey('DGitBranch', on_delete=models.CASCADE,
                                   related_name="%(app_label)s_%(class)s_created", null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name="%(app_label)s_%(class)s_created")
    repository = models.ForeignKey('DGitRepository', on_delete=models.CASCADE,related_name="%(app_label)s_%(class)s_created")
    name = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True)

class DGitRepository(models.Model):
    object_id = models.UUIDField(unique=True, editable=False,
                                 default=uuid.uuid4, verbose_name='Public identifier')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name="%(app_label)s_%(class)s_created")
    name = models.TextField()
    visibilty = models.BooleanField(null=False)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE,
                              related_name="%(app_label)s_%(class)s_created", null=True)

class DGitBlob(models.Model):
    object_id = models.UUIDField(unique=True, editable=False,
                                 default=uuid.uuid4, verbose_name='Public identifier')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name="%(app_label)s_%(class)s_created")
    name = models.TextField()
    path = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True)
    checksum = models.CharField(max_length=20)
    save_path = models.TextField()