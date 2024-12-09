
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms

#new
from django.contrib.auth.forms import SetPasswordForm


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
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

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

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            raise forms.ValidationError("The new passwords do not match.")
        
#new

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Enter your registered email address", widget=forms.EmailInput(attrs={'class': 'input input-bordered w-full'}))

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
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-bordered w-full'}), label="New Password", required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input input-bordered w-full'}), label="Confirm New Password", required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            raise forms.ValidationError("The new passwords do not match.")
        return cleaned_data
