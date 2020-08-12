from django import forms

from .models import Classroom


class ClassroomCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    identifier = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Classroom
        fields = ('classname', 'password', 'identifier')


class ClassroomJoinForm(forms.Form):
    identifier = forms.CharField(max_length=6)

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get('identifier')
        try:
            Classroom.objects.get(identifier=identifier)
        except Classroom.DoesNotExist:
            # print(self.errors.identifier)
            self.errors['identifier'] = ('Incorrect Identifier',)
