from django import forms
from .models import Project
from .models import Task, TaskFile, TaskComment

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'emoji_icon', 'description', 'start_date', 'end_date']

    start_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

<<<<<<< Updated upstream

=======
class MemberCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email','password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        
>>>>>>> Stashed changes
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'priority', 'start_date', 'end_date', 'assigned_members']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border border-gray-300 rounded-md p-2 w-full', 'placeholder': 'Task name'}),
            'description': forms.Textarea(attrs={'class': 'border border-gray-300 rounded-md p-2 w-full h-32', 'placeholder': 'Task description'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'border border-gray-300 rounded-md p-2 w-full'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'border border-gray-300 rounded-md p-2 w-full'}),
            'status': forms.Select(attrs={'class': 'border border-gray-300 rounded-md p-2 w-full'}),
            'priority': forms.Select(attrs={'class': 'border border-gray-300 rounded-md p-2 w-full'}),
            'assigned_members': forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox'}),
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