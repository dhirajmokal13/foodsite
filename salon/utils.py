from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone

# decorators for check is business logged in
def business_login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.session._SessionBase__session_key or request.session['loggedIn'] != True or request.session['type_of_loggedin'] != "Business":
            messages.warning(request, "Please Login As Business")
            return redirect('/salon')
        response = func(request, *args, **kwargs)
        return response
    return wrapper

# decorators for check is user logged in
def user_login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.session._SessionBase__session_key or request.session['loggedIn'] != True or request.session['type_of_loggedin'] != "user":
            messages.warning(request, "Please Login As User")
            return redirect('/salon')
        response = func(request, *args, **kwargs)
        return response
    return wrapper


def get_today_date():
    return timezone.now().date()
