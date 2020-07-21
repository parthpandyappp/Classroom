from django.db import models
from django.contrib.auth.models import User

#class Pswd(models.Model):
#    passcode = models.CharField(max_length=50, null=True)

#    def __str__(self):
#        return self.passcode

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
        )


class classroom(models.Model):
    classname = models.CharField(max_length=50, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    passcode = models.CharField(max_length=50, null=True)
    user_profile = models.ManyToManyField(UserProfile)

    def __str__(self):
        return self.classname