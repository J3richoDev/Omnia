from django import forms
from .models import Project
from .models import Task, TaskFile, TaskComment
from users.models import CustomUser

ICON_CHOICES = [
    ('fa-address-book', 'Address Book'),
    ('fa-calendar', 'Calendar'),
    ('fa-check-circle', 'Check Circle'),
    ('fa-heart', 'Heart'),
]

class ProjectForm(forms.ModelForm):
    emoji_icon = forms.ChoiceField(choices=ICON_CHOICES, required=False,
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Project
        fields = ['name', 'emoji_icon', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AddMemberForm(forms.Form):
    member = forms.ModelChoiceField(queryset=CustomUser.objects.filter(role='member'), required=True)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'priority', 'start_date', 'end_date', 'assigned_members']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'assigned_members': forms.CheckboxSelectMultiple(),
        }

class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['content']

class TaskFileForm(forms.ModelForm):
    class Meta:
        model = TaskFile
        fields = ['file']