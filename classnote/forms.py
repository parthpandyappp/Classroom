from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import UserProfile

from .models import classroom


"""
    User-registration form which extends user model with extra fields
"""


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

        def save(self, commit=True):
            user = super(RegistrationForm, self).save(commit=False)

            if commit:
                user.save()
            return user


class Join(forms.Form):
    join = forms.CharField(
        strip=True, max_length=6,
        required=True, help_text="Enter the unique code here"
    )

    class Meta:
        model = classroom
        fields = [
            'join'
        ]


class UserUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

        def __init__(self):
            super(UserUpdate, self).__init__()


class UserProfileform(forms.Form):
    Description = forms.CharField(max_length=300)

    class Meta:
        fields = [
            'Description',
        ]


class UpdateUserProfileform(forms.Form):
    Description = forms.CharField(max_length=150)

    class Meta:
        model = UserProfile
        fields = [
            'Description',
        ]

        def __init__(self):
            super(UpdateUserProfileform, self).__init__()
