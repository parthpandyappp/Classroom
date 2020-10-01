from classnote.models import classroom
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render

from accounts.forms import (RegistrationForm, UpdateUserProfileform,
                            UserProfileform, UserUpdate)
from accounts.models import UserProfile

"""
    Definitions which registers, logs in, and logs out a user.
"""


class UserLoginView(LoginView):
    template_name = 'registration/login.html'


class UserLogoutView(LogoutView):
    template_name = 'registration/logout.html'


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        profile_form = UserProfileform(request.POST)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            description = profile_form.cleaned_data['Description']
            user = authenticate(username=username, password=password)
            login(request, user)
            profile = UserProfile.objects.get(user=user)
            profile.description = description
            profile.save()
            return redirect('index')
    else:
        form = RegistrationForm()
        profile_form = UserProfileform()

    context = {'form': form, 'profile_form': profile_form}
    return render(request, 'registration/register.html', context)


"""
Below views for Profile details and it's updations
"""


def profile(request):
    desc = UserProfile.objects.get(user=request.user)
    desc = {'desc': desc}
    return render(request, "class/profile.html", desc if desc else None)


def UserUpdatation(request):
    if request.method == 'POST':
        form = UserUpdate(request.POST, instance=request.user)
        profile_form = UserProfileform(request.POST)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            description = profile_form.cleaned_data['Description']
            profile = UserProfile.objects.get(user=request.user)
            profile.description = description
            profile.save()
            # profile_form.save()
            messages.success(request, 'Great, User updated successfully!')
            return render(request, 'class/profile.html', {'profile': profile})
    else:
        form = UserUpdate(instance=request.user)
        des = UserProfile.objects.get(user=request.user)
        profile_form = UserProfileform(
            initial={'Description': des.description})
        args = {}
        args['form'] = form
        args['profile_form'] = profile_form
        return render(request, 'class/edit_profile.html', args)
