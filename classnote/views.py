# -*- coding: utf-8 -*-

import secrets
import string

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView

from accounts.models import UserProfile

from .forms import Join, RegistrationForm, UserUpdate
from .models import classroom


"""
    Renders Home Page of the project.
"""


def index(request):
    if request.user.is_authenticated:
        me = request.user.username
        you = f"Welcome {me}! Enjoy the fun & interactive way of learning!"
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
        name.creator = request.user
        name.code = password
        name.save()
    return render(request, "class/create.html",
                  {'password': password, 'creator': name.creator})


"""
    Render a form which prompts the user to fill in the code to join the class.

    A definition where the checking process is carried out for the passcode.
    If passes, okay.html is rendered and if not then no.html is rendered.
"""


class JoinView(FormView):
    form_class = Join
    template_name = 'class/join2.html'
    success_url = reverse_lazy('join-done')

    def form_valid(self, form):
        join = form.cleaned_data.get('join')
        try:
            classroom_obj = classroom.objects.get(code=join)
        except classroom.DoesNotExist:
            return super(JoinView, self).form_invalid(form)
        classroom_obj.user_profile.add(self.request.user.profile)
        return super(JoinView, self).form_valid(form)


class JoinDoneView(ListView):
    template_name = "class/join-done.html"
    model = UserProfile

    def get_queryset(self):
        classes = classroom.objects.filter(
            user_profile=self.request.user.profile)
        return classes


def join(request):
    if request.method == 'POST':
        form = Join(request.POST)
        if form.is_valid():
            passcode = form.cleaned_data['join']
            try:
                classroom_joined = classroom.objects.get(code=passcode)
            except classroom.DoesNotExist:
                messages.warning(
                    request, 'Sorry, Your password doesn\'t matches')
                return render(request, "class/no.html")

            joinedby = request.user
            classroom_joined.joiners = joinedby
            messages.success(
                request,
                'Welcome! your password has been matched successfully!'
            )
            return render(request, "class/okay.html",
                          {'classrooms': classroom_joined, 'pswd': passcode})

    else:
        form = Join()
        context = {"form": form}

    messages.info(request, 'Enter the unique passcode below')
    return render(request, "class/join.html", context)


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
