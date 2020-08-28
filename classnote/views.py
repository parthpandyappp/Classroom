# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import secrets
import string

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from accounts.models import User
from .forms import RegistrationForm, Join, UserUpdate
from .models import classroom
from django.contrib import messages

"""
    Renders Home Page of the project.
"""

def index(request):
    if request.user.is_authenticated:
        me = request.user.username
        you = "Welcome " + me + " , Enjoy the fun & interactive way of learning!"
        messages.info(request, you)

    return render(request, "class/index.html")

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
        name.creator =  request.user
        name.code = password
        name.save()
    return render(request, "class/create.html", {'password': password, 'creator': name.creator})

"""
    Renders a form which prompts the user to fill in the code to join the class.

    A definition where the checking process is carried out for the passcode.
    If passes, okay.html is rendered and if not then no.html is rendered.
"""
def join(request):
    if request.method == 'POST':
        form = Join(request.POST)
        if form.is_valid():
            passcode = form.cleaned_data['join']
            classrooms = classroom.objects.all()
            print(classrooms)
            joinedby = request.user
            for p in classrooms:
                if(p.code == passcode):
                    classrooms.joiners = joinedby
                    messages.success(request, 'Welcome! your password has been matched successfully!')
                    return render(request, "class/okay.html", {'classrooms': classrooms, 'pswd': passcode})

            else:
                messages.warning(request, 'Sorry, Your password doesn\'t matches')
                return render(request, "class/no.html")

    else:
        form = Join()
        context = {"form":form}

    messages.info(request, 'Enter the unique passcode below')
    return render(request, "class/join.html",context)

"""
    A definition which registers & logs in a user.
"""
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)

"""
    Below views for Profile details and it's updations
"""

def profile(request):
    return render(request, "class/profile.html")

def UserUpdatation(request):
    if request.method == 'POST':
        form = UserUpdate(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Great, User updated successfully!')
            return render(request, 'class/profile.html')
    else:
        form = UserUpdate(instance=request.user)
        args = {}
        args['form'] = form
        return render(request, 'class/edit_profile.html', args)
