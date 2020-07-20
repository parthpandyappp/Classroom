# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Pswd(models.Model):
    passcode = models.CharField(max_length=50, null=True)
    def __str__(self):
        return self.passcode

class classroom(models.Model):
    passcod = models.ForeignKey(Pswd, on_delete=models.CASCADE, null=True)
    classname = models.CharField(max_length=50, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')

    def __str__(self):
        return self.classname
# Create your models here.