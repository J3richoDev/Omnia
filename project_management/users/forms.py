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

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', "The new passwords do not match.")
        return cleaned_data


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