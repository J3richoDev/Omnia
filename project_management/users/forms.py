from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import SetPasswordForm
from .models import CustomUser
from django import forms
from projects.models import ProjectMember

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email")

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username:
            raise forms.ValidationError("Please enter your username or email.")

        if '@' in username:  # Check if input is an email
            try:
                user = CustomUser.objects.get(email=username)
                if not user.is_active:
                    raise forms.ValidationError("This account is inactive.")
                return user.username
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
    old_password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Your old password was entered incorrectly. Please enter it again.")
        return old_password


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Enter your registered email address",
                             widget=forms.EmailInput(attrs={'class': 'input input-bordered w-full'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            if not user.is_active:
                raise forms.ValidationError("This account is inactive.")
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("No user found with this email address.")
        return email


class ResetPasswordForm(SetPasswordForm):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-bordered w-full'}),
                                   label="New Password", required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-bordered w-full'}),
                                       label="Confirm New Password", required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            raise forms.ValidationError("The new passwords do not match.")
        return cleaned_data