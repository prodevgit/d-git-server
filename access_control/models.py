import uuid

from django.conf import settings
from django.db import models

# REPOSITORY_PERMISSIONS = (
#     (1, 'Read'),
#     (2, 'Write'),
#     (3, 'Merge'),
#     (4, 'Delete')
# )

REPOSITORY_ROLES = (
    (1, 'Owner'),
    (2, 'Manager'),
    (3, 'Developer'),
)


class Policy(models.Model):
    object_id = models.UUIDField(unique=True, editable=False,
                                 default=uuid.uuid4, verbose_name='Public identifier')

    created = models.DateTimeField(auto_now_add=True, blank=True)
    permissions = models.ManyToManyField('RepositoryPermission')

class Role(models.Model):
    object_id = models.UUIDField(unique=True, editable=False,
                                 default=uuid.uuid4, verbose_name='Public identifier')
    name = models.TextField()
    role = models.IntegerField(choices = REPOSITORY_ROLES,
                                      default = 1)
    created = models.DateTimeField(auto_now_add=True, blank=True)

class RepositoryPermission(models.Model):
    object_id = models.UUIDField(unique=True, editable=False,
                                 default=uuid.uuid4, verbose_name='Public identifier')
    role =  models.ForeignKey('Role', on_delete=models.CASCADE,
                              related_name="%(app_label)s_%(class)s_created", null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name="%(app_label)s_%(class)s_created", null=True)
    is_read = models.BooleanField(default=False)
    is_write = models.BooleanField(default=False)
    is_merge = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

class RepositoryInvite(models.Model):
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name="%(app_label)s_%(class)s_created", null=True)
    repository = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    expired = models.BooleanField(default=False)

class CloneToken(models.Model):
    token = models.UUIDField(unique=True, editable=False,
                                 default=uuid.uuid4)
    is_valid = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    repository = models.ForeignKey('dgit.DGitRepository', on_delete=models.CASCADE,
                              related_name="%(app_label)s_%(class)s_repository", null=True)