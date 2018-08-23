from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect


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
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
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


def profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile = user.userprofile
    template = 'accounts/profile.html'
    context = {'user': user,
               'profile': profile}
    return render(request, template, context)


def edit_profile(request, user_id):
    pass


def bio(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile = user.userprofile
    template = 'accounts/bio.html'
    context = {'user': user,
               'profile': profile}
    return render(request, template, context)