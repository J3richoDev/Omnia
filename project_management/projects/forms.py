from django import forms
from .models import Project
from .models import Task, TaskFile, TaskComment
from users.models import CustomUser

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'emoji_icon', 'description', 'color']
        widgets = {
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

class MemberCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email','username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email