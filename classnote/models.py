from django.contrib.auth.models import User
from django.db import models

from accounts.models import UserProfile


class Pswd(models.Model):
    passcode = models.CharField(max_length=150)


class classroom(models.Model):
    classname = models.CharField(max_length=50, null=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user', null=True,
        blank=True
    )
    code = models.ForeignKey(
        Pswd, on_delete=models.CASCADE, related_name='code')
    user_profile = models.ManyToManyField(UserProfile)

    def __str__(self):
        return self.classname
