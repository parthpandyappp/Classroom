from django.contrib.auth.models import User
from django.db import models

from accounts.models import UserProfile


class Pswd(models.Model):
    passcode = models.CharField(max_length=150, null=True)
    def __str__(self):
        return self.passcode

class classroom(models.Model):
    classname = models.CharField(max_length=50, null=True)
    #user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user', null=True,blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE,related_name='creator', null=True)
    code = models.ForeignKey(Pswd, on_delete=models.CASCADE, related_name='code',null=True)
    user_profile = models.ManyToManyField(UserProfile)

    def __str__(self):
        return self.classname
