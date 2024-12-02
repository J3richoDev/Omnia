from projects.models import Project

def user_projects(request):
    if request.user.is_authenticated:
        projects = Project.objects.filter(owner=request.user)
        return {'user_projects': projects}
    return {}
