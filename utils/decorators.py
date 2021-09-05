from functools import wraps


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