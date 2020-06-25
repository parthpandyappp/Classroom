# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class Pswd(models.Model):
    passcode = models.CharField(max_length=50)
# Create your models here.
