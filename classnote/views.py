import secrets
import string

from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView

from classnote.forms import Join
from classnote.models import classroom


def index(request):
    """
        Renders Home Page of the project.
    """
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


def create(request):
    """
        Renders a form prompting user for classname and related credentials.
    """
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


def join(request):
    """ This view is not used anymore- please delete it. """
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


class JoinView(FormView):
    """
    Renders a form which prompts the user to fill in the code to join the class.
    A definition where the checking process is carried out for the passcode.
    If passes, okay.html is rendered and if not then no.html is rendered.
    """
    template_name = 'class/join.html'
    form_class = Join
    success_url = reverse_lazy('classnote:okay')

    def form_valid(self, form):
        passcode = form.cleaned_data['join']
        try:
            classroom_obj = classroom.objects.get(code=passcode)
        except classroom.DoesNotExist:
            return self.form_invalid(form)
        if classroom_obj in self.request.user.profile.classroom_set.all():
            messages.error(self.request, 'You are already in that class')
        else:
            classroom_obj.user_profile.add(self.request.user.profile)
            messages.success(self.request, 'You were added to class successfully!')
        return super(JoinView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'You have added incorrect passcode')
        return super(JoinView, self).form_invalid(form)


class JoinOkayView(ListView):
    model = classroom
    template_name = 'class/okay.html'

    def get_queryset(self):
        return self.request.user.profile.classroom_set.all()
