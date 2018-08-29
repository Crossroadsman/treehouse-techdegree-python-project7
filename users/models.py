from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser
)
from django.db import models


class P7UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """Creates and saves a user woth the specified email and password"""
        if not email:
            raise ValueError("Users must provide an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class P7User(AbstractBaseUser):
    """For our custom user we are including only those fields that are strictly
    necessary for authentication. All other fields will be in the Profile
    model that will be one-to-one linked with this model"""
    email = models.EmailField(
        verbose_name='Email Address',
        max_length=255,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # note the following is an attribute, not a field
    objects = P7UserManager()

    # the following attribute specifies which of our fields should be the
    # unique identifier for users. In this case, based on our selections above
    # either `email` or `username` could be valid choices for this attribute
    USERNAME_FIELD = 'email'

    # the following is a list of fields that are passed through to the 
    # create_superuser method (other than USERNAME_FIELD and password)
    # when using (e.g.) `python3 manage.py createsuperuser`
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
