# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Pswd, classroom
import secrets
import string

def index(request):
    return render(request, "index.html")

def create(request):
    return render(request, "upload.html")

def processing(request):
    alphabet = string.ascii_letters + string.digits 
    password = ''.join(secrets.choice(alphabet) for i in range(6))
    form = Pswd()
    form.passcode = password
    form.save()
    if request.method == "POST" :
        name = classroom()
        name.classname = request.POST.get('class_name')
        name.passcod = Pswd.objects.last()
        name.save()
    return render(request, "create.html", {'password':password})

def join(request):
    return render(request, "join.html")

def check(request):
    if request.method == "POST" :
        pswrd = Pswd.objects.all()
        pswd = request.POST.get('passcode')
        q = pswrd[len(pswrd)-1]
        print(q.passcode)
        for p in pswrd :
            print(p.passcode)
            # print(pswd)
            if(p.passcode == pswd) :
                return render(request, "okay.html")

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

    context = {'form' : form}
    return render(request, 'registration/register.html', context)