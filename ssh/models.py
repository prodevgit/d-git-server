import uuid

from django.conf import settings
from django.db import models

# Create your models here.

class SSHToken(models.Model):
    token = models.UUIDField(unique=True, editable=False,
                                 default=uuid.uuid4)
    is_valid = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)

class UserSSH(models.Model):
    object_id = models.UUIDField(unique=True, editable=False,
                                 default=uuid.uuid4, verbose_name='Public identifier')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name="%(app_label)s_%(class)s_created")
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    