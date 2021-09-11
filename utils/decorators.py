from functools import wraps

from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.response import Response

from ssh.models import SSHToken


def merge_guard(function):
  @wraps(function)
  def wrap(request, *args, **kwargs):
        user = request.user
        if request.usertype == 'Author':
             return function(request, *args, **kwargs)
        else:
            data = {}
            data['status'] = False
            data['message'] = "You don't have required permissions to delete"
            return data

  return wrap

def repo_auth(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        token = request.META['HTTP_AUTHORIZATION']
        clone_by = request.GET.get('clone_by')
        if clone_by == 'ssh':
            ssh_token = SSHToken.objects.filter(token=token,is_valid=True).first()
            if ssh_token:
                return function(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('api:repository-unauthorized-clone-api'))
        else:
            return HttpResponseRedirect(reverse('api:repository-unauthorized-clone-api'))

    return wrap