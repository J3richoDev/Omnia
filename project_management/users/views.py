from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, logout, authenticate, login
from django.contrib import messages
from .forms import CustomUserCreationForm, MemberCreationForm, MemberProfileForm, UserUpdateForm, PasswordChangeForm, CustomAuthenticationForm, ForgotPasswordForm, ResetPasswordForm
from .models import CustomUser
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = request.POST.get('password')

            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username/email or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'users/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Replace with your login URL
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def create_member(request):
    if request.user.role != CustomUser.MANAGER:
        return redirect('dashboard')  # Restrict access to managers

    if request.method == 'POST':
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.role = CustomUser.MEMBER
            member.set_password(form.cleaned_data['password'])
            member.save()
            return redirect('members_list')  # Replace with your members list URL
    else:
        form = MemberCreationForm()
    return render(request, 'users/create_member.html', {'form': form})

@login_required
def complete_profile(request):
    if request.method == 'POST':
        form = MemberProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('dashboard')  # Redirect to the dashboard
    else:
        form = MemberProfileForm(instance=request.user)
    return render(request, 'users/complete_profile.html', {'form': form})

@login_required
def my_profile(request):
    user = request.user

    # Initialize the forms with the user's data
    user_form = UserUpdateForm(instance=user)
    password_form = PasswordChangeForm()
    context = {
        "user_form": user_form,
        "password_form": password_form,
    }

    if request.method == "POST":
        if "save_profile" in request.POST:
            # Handle profile picture update
            user_form = UserUpdateForm(request.POST, request.FILES, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Profile picture updated successfully!")
                return redirect("my_profile")

        elif "update_info" in request.POST:
            # Handle general user info update
            user_form = UserUpdateForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "Info changed successfully!")
                return redirect("my_profile")

        elif "change_password" in request.POST:
            # Handle password change
            password_form = PasswordChangeForm(request.POST)
            if password_form.is_valid():
                old_password = password_form.cleaned_data["old_password"]
                new_password = password_form.cleaned_data["new_password"]

                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Password changed successfully!")
                    update_session_auth_hash(request, user)  # Keep user logged in
                    return redirect("my_profile")
                else:
                    password_form.add_error("old_password", "Old password is incorrect.")

    context["user_form"] = user_form
    context["password_form"] = password_form
    return render(request, "users/my_profile.html", context)

def logout_view(request):
    logout(request)
    return redirect('login')


# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')

#         if email:
#             try:
#                 user = CustomUser.objects.get(email=email)

#                 token = default_token_generator.make_token(user)
#                 uid = urlsafe_base64_encode(str(user.pk).encode())

#                 reset_url = f"http://{get_current_site(request).domain}/reset-password/{uid}/{token}/"

#                 send_mail(
#                     "Password Reset Request",
#                     f"Click the link to reset your password: {reset_url}",
#                     "no-reply@omnia.com",
#                     [email],
#                 )

#                 messages.success(request, "A password reset link has been sent to your email address.")
#                 return redirect('login')
#             except CustomUser.DoesNotExist:
#                 messages.error(request, "No user found with that email address.")
#         else:
#             messages.error(request, "Please provide a valid email address.")

#     return render(request, 'users/forgotpass.html')
def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)

                # Generate token and URL for password reset
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(str(user.pk).encode())
                # Generate the password reset URL
                reset_url = f"http://{get_current_site(request).domain}/reset-password/{uid}/{token}/"
                # Send email
                send_mail(
                    subject="Password Reset Request",
                    message=f"Click the link to reset your password: {reset_url}",
                    from_email="no-reply@omnia.com",  # Replace with your email address
                    recipient_list=[email],
                )
                messages.success(request, "A password reset link has been sent to your email address.")
                return redirect('login')
            except CustomUser.DoesNotExist:
                messages.error(request, "No user found with that email address.")
        else:
            messages.error(request, "Please provide a valid email address.")
    else:
        form = ForgotPasswordForm()
    return render(request, 'users/forgotpass.html', {'form': form})


def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = ResetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been reset successfully!")
                return redirect('login')
        else:
            form = ResetPasswordForm(user)
    else:
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect('login')

    return render(request, 'users/reset_password.html', {'form': form})
# def reset_password(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = CustomUser.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
#         user = None

#     if user and default_token_generator.check_token(user, token):
#         if request.method == 'POST':
#             form = SetPasswordForm(user, request.POST)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, "Your password has been reset successfully!")
#                 return redirect('login')
#         else:
#             form = SetPasswordForm(user)
#     else:
#         messages.error(request, "The reset link is invalid or has expired.")
#         return redirect('login')

#     return render(request, 'users/reset_password.html', {'form': form})