from django.contrib.auth.models import User
from django.db import models

from accounts.models import UserProfile


class Classroom(models.Model):
    classname = models.CharField(max_length=50, null=True)
    creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
    related_name='creator_profile')
    password = models.CharField(max_length=150)

    def __str__(self):
        return self.classname
