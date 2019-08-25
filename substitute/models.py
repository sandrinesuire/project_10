"""
Models
"""

from django.contrib.auth.models import User
from django.db import models


class User(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "Profil de {0}".format(self.user.username)
