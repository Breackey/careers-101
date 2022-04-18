from django.core.exceptions import PermissionDenied


def user_is_recruiter(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role == 'recruiter':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_candidate(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role == 'candidate':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_superuser(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.role == 'superuser':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap