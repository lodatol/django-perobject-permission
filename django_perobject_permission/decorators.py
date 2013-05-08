# -*- coding: utf-8 -*-
try:
    from urllib.parse import urlparse
except ImportError: # Python 2
    from urlparse import urlparse
from functools import wraps
import inspect

from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.utils.decorators import available_attrs
from django.utils.encoding import force_str
from django.shortcuts import resolve_url



def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            # I need to pass kwargs to test_func for extract the model pk from url
            if test_func(request.user, *args, **kwargs):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            # urlparse chokes on lazy objects in Python 3, force to str
            resolved_login_url = force_str(
                resolve_url(login_url or settings.LOGIN_URL))
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator


def object_permission_required(func, view_param_pk='pk', login_url=None, raise_exception=False):
    def check_perms(user, *args, **kwargs):
        obj = get_object_or_404(func.im_class, pk = kwargs[view_param_pk])

        if (len(inspect.getargspec(func)[0]) == 2):
            is_authorized = func(obj, user)
        else:
            is_authorized = func(obj)
        if not isinstance(is_authorized, bool):
            raise NotBooleanPermission("Callable from model %s on rule %s does not return a boolean value",
                                        (rule.model, rule.func.__name__))
        if is_authorized:
            return True

        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms, login_url=login_url)
