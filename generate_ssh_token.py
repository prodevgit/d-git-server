import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DGitServer.settings")

import django
django.setup()

from access_control.models import CloneToken
import sys
from django.contrib.auth.models import User
from dgit.models import DGitRepository

# sshtoken = SSHToken.objects.create()
# print(sshtoken.token)
repository = sys.argv[1]
user,repository = repository.split('/')
try:
    user = User.objects.get(username=user)
    repository = DGitRepository.objects.get(owner=user,name=repository)
    cloneToken = CloneToken.objects.create(repository=repository)
    print('{"status":"True","data":"'+str(cloneToken.token)+'"}')
except DGitRepository.DoesNotExist as e:
    print('{"status":"False","message":"Repository does not exists"}')
except User.DoesNotExist as e:
    print('{"status":"False","message":"User does not exists"}')
except Exception as e:
    print('{"status":"False","message":"Unknown Error"}')
