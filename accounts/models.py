import os

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField

def user_avatar_path(instance, filename):
    """See django.db.models.FileField in the django docs
    
    `instance` is the object with the ImageField;
    `filename` is the file's original filename
    """
    username = instance.user_id
    _, ext = os.path.splitext(filename)
    return 'avatars/{}{}'.format(username, ext)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE
    )

    date_of_birth = models.DateField()
    bio = RichTextField()

    # Optional Fields:
    given_name = models.CharField(max_length=255,
                                  blank=True,
                                  default='')
    family_name = models.CharField(max_length=255,
                                  blank=True,
                                  default='')

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
        prefix = ""
        suffix = ""
        if self.given_name:
            prefix += self.given_name + " "
        if self.family_name:
            prefix += str(self.family_name).upper() + " "
        if prefix:
            prefix += "("
            suffix = ")"
        return prefix + self.user.email + suffix

    def get_absolute_url(self):
        return reverse('accounts:profile', 
                       kwargs={'user_id': self.user_id,})
