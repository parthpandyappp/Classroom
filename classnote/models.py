from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Pswd(models.Model):
    passcode = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.passcode

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True, blank=True)
    
    def __str__(self):
        return self.user.username

class classroom(models.Model):
    classname = models.CharField(max_length=50, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    code = models.ForeignKey(Pswd, on_delete=models.CASCADE, null=True)
    user_profile = models.ManyToManyField(UserProfile)

    def __str__(self):
        return self.classname



"""def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)"""
