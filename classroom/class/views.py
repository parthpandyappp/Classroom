# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Pswd
import secrets
import string

def index(request):
    return render(request, "index.html")

def create(request):
    alphabet = string.ascii_letters + string.digits 
    password = ''.join(secrets.choice(alphabet) for i in range(6))
    form = Pswd()
    form.passcode = password
    form.save()
    return render(request, "create.html", {'password':password})

def join(request):
    return render(request, "join.html")

def check(request):
    if request.method == "POST" :
        pswrd = Pswd.objects.all()
        pswd = request.POST.get('passcode')
        for p in pswrd :
            print(p.passcode)
            print(pswd)
            if(p.passcode == pswd) :
                return render(request, "okay.html")

            else :
                return render(request, "no.html")
        
# Create your views here.