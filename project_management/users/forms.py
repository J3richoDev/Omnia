from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms
from projects.models import ProjectMember

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if '@' in username:  # Check if input is an email
            try:
                user = CustomUser.objects.get(email=username)
                if not user.is_active:
                    raise forms.ValidationError("This account is inactive.")
                return user.username  # Ensure it returns a string (correct)
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("No user found with this email address.")
        return username


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']

class MemberCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email','username', 'password', 'profile_picture']
        widgets = {
            'password': forms.PasswordInput(),
        }
    def __init__(self, project=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 5 * 1024 * 1024:  # 5 MB limit
                raise forms.ValidationError("The profile picture size should not exceed 5MB.")
            if not picture.content_type.startswith("image/"):
                raise forms.ValidationError("Only image files are allowed.")
        return picture
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create ProjectMember instance
            ProjectMember.objects.create(project=self.project, user=user)
        return user 
    
class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_picture']
       

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-class-old w-1/ border rounded px-3 py-2'}), required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-class-new  w-1/3 border rounded px-3 py-2'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-class-confirm  w-1/3    border rounded px-3 py-2'}), required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            raise forms.ValidationError("The new passwords do not match.")