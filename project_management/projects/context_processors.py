from projects.models import Project

def user_projects(request):
    if request.user.is_authenticated:
        return {'user_projects': Project.objects.filter(owner=request.user)}
    return {}
