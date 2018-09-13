from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout, get_user_model,
                                 update_session_auth_hash)
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect

from html_sanitizer import Sanitizer

from users.forms import (P7UserCreationForm, P7UserChangeForm,
                         PasswordChangeForm)
from accounts.models import UserProfile
from accounts.forms import UserProfileForm



def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return redirect(
                        reverse('home')  # TODO: go to profile
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = P7UserCreationForm()
    if request.method == 'POST':
        form = P7UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return redirect(reverse('home'))  # TODO: go to profile
    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return redirect(reverse('home'))


def profile(request):
    user = get_object_or_404(get_user_model(), pk=request.user.pk)
    if not hasattr(user, 'userprofile'):
        return redirect(reverse('accounts:edit_profile'))
    profile = user.userprofile
    template = 'accounts/profile.html'
    context = {'user': user,
               'profile': profile}
    return render(request, template, context)


def edit_profile(request):
    user = get_object_or_404(get_user_model(), pk=request.user.pk)
    if hasattr(user, 'userprofile'):
        up_instance = user.userprofile
    else:
        up_instance = None
    if request.method == "POST":
        user_form = P7UserChangeForm(request.POST, instance=user, initial={'confirm_email': user.email})
        profile_form = UserProfileForm(request.POST, request.FILES, instance=up_instance)
        if all([user_form.is_valid(),
                profile_form.is_valid()]):
            user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            sanitizer = Sanitizer()
            profile.bio = sanitizer.sanitize(profile.bio)
            profile.save()
            return redirect(reverse('accounts:profile'))
    
    else:  # GET
        user_form = P7UserChangeForm(instance=user, initial={'confirm_email': user.email})
        profile_form = UserProfileForm(instance=up_instance)
    
    template = 'accounts/edit_profile.html'
    context = {'user_form': user_form,
               'profile_form': profile_form}
    return render(request, template, context)
        

def bio(request):
    user = get_object_or_404(get_user_model(), pk=request.user.pk)
    profile = user.userprofile
    template = 'accounts/bio.html'
    context = {'user': user,
               'profile': profile}
    return render(request, template, context)


def change_password(request):
    user = request.user
    form = PasswordChangeForm(user)
    if request.method == "POST":
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            u = form.save()
            update_session_auth_hash(request, u)
            messages.success(request, "Password successfully changed")
            return redirect(reverse('accounts:profile'))
    template = 'accounts/change_password.html'
    context = {'form': form}
    return render(request, template, context)
