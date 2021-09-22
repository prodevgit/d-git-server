import uuid

from django.conf import settings
from django.db import models


LOG_TYPES = (
    (1, 'Commit'),
    (2, 'Push'),
    (3, 'Branch'),
    (4, 'Access'),
    (5, 'Repository'),
    (6, 'Settings')
)

class DGitLog(models.Model):
    object_id = models.UUIDField(unique=True, editable=False,
                                 default=uuid.uuid4, verbose_name='Public identifier')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name="%(app_label)s_%(class)s_owner")
    created = models.DateTimeField(auto_now_add=True, blank=True)
    type = models.IntegerField(choices = LOG_TYPES, blank= True)
    data = models.TextField()
