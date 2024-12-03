from django.shortcuts import redirect

class FirstTimeLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only proceed if the user is authenticated
        if request.user.is_authenticated:
            if request.user.role == 'member' and not request.user.email:
                # If the member has no email, redirect to complete profile
                if not request.path.startswith('/users/complete-profile/'):
                    return redirect('complete_profile')
            elif request.user.role == 'manager' and request.user.is_first_login:
                # If the manager is logging in for the first time, redirect to create project
                if not request.path.startswith('/projects/create/'):
                    return redirect('create_project')
        # For non-authenticated users (like after logout) or if no conditions match
        return self.get_response(request)
