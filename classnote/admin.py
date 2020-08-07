# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Pswd, classroom

admin.site.register(classroom)
admin.site.register(Pswd)
