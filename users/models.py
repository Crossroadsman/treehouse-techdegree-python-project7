from django.contrib import auth
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    Permission,
    Group
)
from django.core.exceptions import PermissionDenied
from django.db import models


class P7UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """Creates and saves a user with the specified email and password"""
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
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="users",
        blank=True,
    )
    groups = models.ManyToManyField(
        Group,
        related_name="users",
        blank=True,
    )

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

    def has_perm(self, perm, obj=None):
        """As per the django src:
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise check the backends
        for backend in auth.get_backends():
            if not hasattr(backend, 'has_perm'):
                continue
            try:
                if backend.has_perm(self, perm, obj):
                    return True
            except PermissionDenied:
                return False
        return False

    def has_module_perms(self, app_label):
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise check the backends
        for backend in auth.get_backends():
            if not hasattr(backend, 'has_module_perms'):
                continue
            try:
                if backend.has_module_perms(self, app_label):
                    return True
            except PermissionDenied:
                return False
        return False
