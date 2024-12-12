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
        fields = ['email','username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        } 
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
    
   
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
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-class-old w-2/3 border rounded px-3 py-2'}),
            'email': forms.EmailInput(attrs={'class': 'input-class-old w-2/3 border rounded px-3 py-2'}),
            'first_name': forms.TextInput(attrs={'class': 'input-class-old w-2/3 border rounded px-3 py-2'}),
            'last_name': forms.TextInput(attrs={'class': 'input-class-old w-2/3 border rounded px-3 py-2'}),
            'profile_picture': forms.FileInput(attrs={'class': 'input-class-old w-2/3 border rounded px-3 py-2'}),
        }
    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 5 * 1024 * 1024:  # 5 MB limit
                raise forms.ValidationError("The profile picture size should not exceed 5MB.")
            valid_mime_types = ["image/jpeg", "image/png"]
            if picture.content_type not in valid_mime_types:
                raise forms.ValidationError("Only JPEG and PNG files are allowed.")
        return picture

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-class-old w-2/3 border rounded px-3 py-2'}), required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-class-new  w-2/3 border rounded px-3 py-2'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-class-confirm  w-2/3    border rounded px-3 py-2'}), required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            raise forms.ValidationError("The new passwords do not match.")