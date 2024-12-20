from projects.models import Project, Notification
from .forms import ProjectForm

def user_projects(request):
    if request.user.is_authenticated:
        if request.user.role == 'manager':
            projects = Project.objects.filter(owner=request.user)
            return {'user_projects': projects}
        else:
            projects = request.user.assigned_projects.all()
            return {'user_projects': projects}
    return {}

def global_forms(request):
    colors = ['purple','red','blue','green','teal','yellow','orange','pink','gray',
    ]

    icons = ['fa-star', 'fa-heart', 'fa-bell', 'fa-check', 'fa-cog', 'fa-user', 'fa-pencil-alt', 'fa-trash',
             'fa-envelope', 'fa-search',
             'fa-plus', 'fa-minus', 'fa-cogs', 'fa-tasks', 'fa-download', 'fa-upload', 'fa-share', 'fa-comments',
             'fa-users',
             'fa-thumbs-up', 'fa-cog', 'fa-home', 'fa-calendar', 'fa-clock', 'fa-wrench', 'fa-flag', 'fa-list',
             'fa-folder',
             'fa-bookmark', 'fa-link', 'fa-map-marker-alt', 'fa-clipboard', 'fa-braille', 'fa-bicycle', 'fa-car',
             'fa-cogs',
             'fa-database', 'fa-paint-brush', 'fa-key', 'fa-gift', 'fa-cloud', 'fa-cloud-upload-alt', 'fa-file',
             'fa-file-alt',
             'fa-comments', 'fa-briefcase', 'fa-cogs', 'fa-paper-plane', 'fa-bolt', 'fa-lightbulb', 'fa-shield-alt']
    return {'project_form': ProjectForm(), 'icons':icons, 'colors':colors}

def global_notifications(request):
    if request.user.is_authenticated:
        # Fetch the latest 5 notifications and unread count for the logged-in user
        notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')[:5]
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {
            'global_notifications': notifications,
            'unread_notification_count': unread_count,
        }
    return {}