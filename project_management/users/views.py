from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import MemberCreationForm
from .forms import MemberProfileForm
from .models import CustomUser

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
