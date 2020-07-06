# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class Pswd(models.Model):
    passcode = models.CharField(max_length=50)

    def __str__(self):
        return self.passcode

class classroom(models.Model):
    classname = models.CharField(max_length=50)

    def __str__(self):
        return self.classname
# Create your models here.
