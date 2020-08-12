from django import forms

from .models import Classroom


class ClassroomCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    identifier = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Classroom
        fields = ('classname', 'password', 'identifier')
