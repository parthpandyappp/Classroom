from django import forms
from .models import Classroom

class ClassroomCreateForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	
	class Meta:
		model = Classroom
		fields = ('classname', 'password')