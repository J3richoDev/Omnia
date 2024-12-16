from django.contrib.messages.context_processors import messages
from django.shortcuts import redirect
from django.contrib import messages

class FirstTimeLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.role == 'member' and not request.user.first_name:
                if not request.path.startswith('/users/my-profile/'):
                    messages.error(request, "Complete Profile to continue.", extra_tags='alert-info')
                    return redirect('my_profile')
            if request.user.role == 'manager' and request.user.is_first_login:
                if not request.path.startswith('/projects/setup/'):
                    return redirect('initial_setup')
        return self.get_response(request)

