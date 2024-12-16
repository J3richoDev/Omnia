from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from .models import Task, Project, Notification
from users.models import CustomUser

@receiver(user_logged_in)
def set_current_project(sender, request, user, **kwargs):
    if user.role == 'manager':
        latest_project = Project.objects.filter(owner=user).order_by('-created_at').first()
        if latest_project:
            request.session['current_project_id'] = latest_project.id  # Save the project ID in the session
        else:
            request.session['current_project_id'] = None
    else:
        # Set the first project the member is involved in
        request.session['current_project_id'] = None


