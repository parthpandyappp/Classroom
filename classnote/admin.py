# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Pswd, classroom, UserProfile
from django.contrib import admin

admin.site.register(Pswd)
admin.site.register(classroom)
admin.site.register(UserProfile)
# Register your models here.

