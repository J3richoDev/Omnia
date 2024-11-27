from django import forms
from .models import Project
from .models import Task, TaskFile, TaskComment

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'emoji_icon', 'description', 'start_date', 'end_date']

    start_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'priority', 'start_date', 'end_date', 'assigned_members']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'assigned_members': forms.CheckboxSelectMultiple(),
        }
    start_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['content']

class TaskFileForm(forms.ModelForm):
    class Meta:
        model = TaskFile
        fields = ['file']