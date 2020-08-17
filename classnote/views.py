# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import secrets
import string

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from accounts.models import User
from .forms import RegistrationForm
from .models import Pswd, classroom

"""
    Renders Home Page of the project.
"""
def index(request):
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
    form = Pswd()
    form.passcode = password
    form.save()
    if request.method == "POST":
        name = classroom()
        name.classname = request.POST.get('class_name')
        name.creator =  request.user
        name.code = Pswd.objects.last()
        name.save()
    return render(request, "class/create.html", {'password': password, 'creator': name.creator})

"""
    Renders a form which prompts the user to fill in the code to join the class.
"""
def join(request):
    return render(request, "class/join.html")

"""
    A definition where the checking process is carried out for the passcode.
    If passes, okay.html is rendered and if not then no.html is rendered.
"""
def check(request):
    if request.method == "POST":
        pswrd = Pswd.objects.all()
        pswd = request.POST.get('passcode')
        pswd = pswd.replace(" ", "")
        q = pswrd[len(pswrd)-1]
        print(q.passcode)
        for p in pswrd:
            print(p.passcode)
            # print(pswd)
            if(p.passcode == pswd):
                classrooms = classroom.objects.all()
                return render(request, "class/okay.html", {'classrooms': classrooms, 'pswd': pswd})

        return render(request, "class/no.html")

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
