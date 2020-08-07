# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import secrets
import string

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from .models import Pswd, classroom


def index(request):
    return render(request, "class/index.html")


def create(request):
    return render(request, "class/upload.html")


def processing(request):
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(6))
    form = Pswd()
    form.passcode = password
    form.save()
    if request.method == "POST":
        name = classroom()
        name.classname = request.POST.get('class_name')
        name.code = Pswd.objects.last()
        name.save()
    return render(request, "class/create.html", {'password': password})


def join(request):
    return render(request, "class/join.html")


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
                return render(request, "class/okay.html",
                              {'classrooms': classrooms, 'pswd': pswd})

        return render(request, "class/no.html")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)
