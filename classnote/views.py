# -*- coding: utf-8 -*-

import secrets

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from .forms import ClassroomCreateForm, ClassroomJoinForm
from .models import Classroom


def index(request):
    return render(request, "classnote/index.html")


# def create(request):
#     return render(request, "classnote/upload.html")


# def processing(request):
#     alphabet = string.ascii_letters + string.digits
#     password = ''.join(secrets.choice(alphabet) for i in range(6))
#     form = Pswd()
#     form.passcode = password
#     form.save()
#     if request.method == "POST":
#         name = classroom()
#         name.classname = request.POST.get('class_name')
#         name.code = Pswd.objects.last()
#         name.save()
#     return render(request, "classnote/create.html", {'password': password})


class ClassroomCreateView(CreateView):
    model = Classroom
    form_class = ClassroomCreateForm
    template_name = 'classnote/classroom_form.html'
    success_url = reverse_lazy('index')

    def get_initial(self):
        initial = super(ClassroomCreateView, self).get_initial()
        initial['identifier'] = secrets.token_urlsafe()[:6]
        return initial

    def form_valid(self, form):
        new_classroom = form.instance
        new_classroom.creator = self.request.user.profile
        return super(ClassroomCreateView, self).form_valid(form)


class ClassroomJoinView(FormView):
    form_class = ClassroomJoinForm
    template_name = 'classnote/class_join.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        profile = self.request.user.profile
        identifier = form.cleaned_data.get('identifier')
        classroom = Classroom.objects.filter(identifier=identifier)
        profile.classrooms.set(classroom)
        return super(ClassroomJoinView, self).form_valid(form)


# def join(request):
#     return render(request, "classnote/join.html")


# def check(request):
#     if request.method == "POST":
#         pswrd = Pswd.objects.all()
#         pswd = request.POST.get('passcode')
#         pswd = pswd.replace(" ", "")
#         q = pswrd[len(pswrd)-1]
#         print(q.passcode)
#         for p in pswrd:
#             print(p.passcode)
#             # print(pswd)
#             if(p.passcode == pswd):
#                 classrooms = classroom.objects.all()
#                 return render(request, "classnote/okay.html",
#                               {'classrooms': classrooms, 'pswd': pswd})

#         return render(request, "class/no.html")


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
