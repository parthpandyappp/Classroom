from django.contrib.auth.models import User
from django.db import models

from accounts.models import UserProfile

"""
    Model for storing unique pass-code, and performing queries
    simply related to password handling.
"""
# class Pswd(models.Model):
#     passcode = models.CharField(max_length=150, null=True)
#     def __str__(self):
#         return self.passcode

"""
                        | Main model of this project |
    Model class for storing classname, class_creator, passcode reference & user_profile
    Here a field needs to be added which references all the users who have joined a
    particular class.
"""


class classroom(models.Model):
    classname = models.CharField(max_length=50, null=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='creator', null=True
    )
    code = models.CharField(max_length=6, null=False, default="passwd")
    user_profile = models.ManyToManyField(UserProfile)

    def __str__(self):
        return self.classname
