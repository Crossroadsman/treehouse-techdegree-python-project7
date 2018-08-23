import os

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


def user_avatar_path(instance, filename):
    """See django.db.models.FileField in the django docs
    
    `instance` is the object with the ImageField;
    `filename` is the file's original filename
    """
    username = instance.user.username
    _, ext = os.path.splitext(filename)
    return 'avatars/{}{}'.format(username, ext)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    date_of_birth = models.DateField()
    bio = models.TextField()

    # Optional Fields:
    avatar = models.ImageField(
        upload_to=user_avatar_path,
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )
    state = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )
    country = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )

    favourite_animal = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )
    hobby = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )
    favourite_fountain_pen = models.CharField(
        max_length=255,
        blank=True,
        default=''
    )

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('accounts:profile', 
                       kwargs={'user_id': self.user.pk,})
