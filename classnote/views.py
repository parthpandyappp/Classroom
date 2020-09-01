# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import secrets
import string

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from accounts.models import UserProfile

from .forms import (Join, RegistrationForm, UpdateUserProfileform,
                    UserProfileform, UserUpdate)
from .models import classroom


"""
    Renders Home Page of the project.
"""


def index(request):
    data = None
    if request.user.is_authenticated:
        me = request.user.username
        you = f"Welcome {me}, enjoy the fun & interactive way of learning!"
        messages.info(request, you)

        classes = classroom.objects.filter(
            user_profile__exact=request.user.profile
        )
        data = {'object_list': classes}

    return render(request, "class/index.html", data if data else None)


"""
    Renders a form prompting user for classname and related credentials.
"""


def create(request):
    return render(request, "class/upload.html")


"""
    A definition where the unique pass-code is being generated, stored
    and displayed at the interface create.html  from where mentor can
    copy that unique text and share it among their students.
"""


def processing(request):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(6))
    if request.method == "POST":
        name = classroom()
        name.classname = request.POST.get('class_name')
        name.creator = request.user
        name.code = password
        name.save()
    return render(request, "class/create.html", {'password': password, 'creator': name.creator, 'name': name.classname})


"""
    Renders a form which prompts the user to fill in the code to join the class.

    A definition where the checking process is carried out for the passcode.
    If passes, okay.html is rendered and if not then no.html is rendered.
"""


def join(request):
    context = None
    if request.method == 'POST':
        form = Join(request.POST)
        if form.is_valid():
            passcode = form.cleaned_data['join']
            classrooms = classroom.objects.all()
            print(classrooms)
            try:
                classroom_obj = classroom.objects.get(code=passcode)
            except classroom.DoesNotExist:
                messages.warning(
                    request, 'Sorry, Your password doesn\'t match'
                )
                return render(request, "class/no.html")

            classroom_obj.user_profile.add(request.user.profile)
            messages.success(
                request, 'Welcome! Your password was matched successfully!'
            )
            return render(
                request, "class/okay.html",
                {'classrooms': classrooms, 'pswd': passcode}
            )

    else:
        form = Join()
        context = {"form": form}

    messages.info(request, 'Enter the unique passcode below')
    return render(request, "class/join.html", context if context else None)


"""
    A definition which registers & logs in a user.
"""


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
    desc = None
    desc = UserProfile.objects.get(user=request.user)
    desc = {'desc':desc}
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
            #profile_form.save()
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