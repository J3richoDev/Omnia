from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.core.serializers import serialize
from .models import Task
from django.contrib.auth.signals import user_logged_in
from .models import Project

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
