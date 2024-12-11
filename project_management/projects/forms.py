from django import forms
from django.core.exceptions import ValidationError
from .models import Project
from .models import Task, TaskFile, TaskComment, Sprint
from users.models import CustomUser

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'emoji_icon', 'description', 'color']
        widgets = {
        }

class AddMemberForm(forms.Form):
    member = forms.ModelChoiceField(queryset=CustomUser.objects.filter(role='member'), required=True)

class SprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = ['name', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        # Capture the project to check the start date uniqueness within a specific project
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')

        if self.project:
            # Ensure the start date is unique within the given project
            if Sprint.objects.filter(project=self.project, start_date=start_date).exists():
                raise forms.ValidationError("A sprint already exists with this start date in the current project.")

        return start_date

    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        # Ensure that start_date and end_date are valid
        if not start_date or not end_date:
            raise forms.ValidationError("Both start date and end date are required.")

        # Ensure the end_date is after the start_date
        if end_date <= start_date:
            raise forms.ValidationError("End date must be later than the start date.")

        return end_date


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