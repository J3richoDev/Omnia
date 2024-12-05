from django.shortcuts import redirect

class FirstTimeLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.role == 'member' and not request.user.email:
                if not request.path.startswith('/users/complete-profile/'):
                    return redirect('complete_profile')
            if request.user.role == 'manager' and request.user.is_first_login:
                if not request.path.startswith('/projects/setup/'):
                    return redirect('initial_setup')
        return self.get_response(request)

