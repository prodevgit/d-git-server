import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DGitServer.settings")
import django
django.setup()
from ssh.models import SSHToken

sshtoken = SSHToken.objects.create()
print(sshtoken.token)



