from functools import wraps

from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.response import Response

from access_control.models import CloneToken
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
        clone_token = CloneToken.objects.filter(token=token,is_valid=True).first()
        if clone_token:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('api:repository-unauthorized-clone-api'))

    return wrap