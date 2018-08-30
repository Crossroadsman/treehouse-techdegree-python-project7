from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (UserCreationForm,
                                       UserChangeForm)


# The purpose of this class is to override the builtin version
# (https://github.com/django/django/blob/master/django/contrib/auth/forms.py)
# so that
# we can customise it. In this case we are:
# - adding an email address field (and setting the label text for the email
#   field)
class P7UserCreationForm(UserCreationForm):
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password, again",
                                widget=forms.PasswordInput)

    class Meta:
        fields = ("email",)
        model = get_user_model()

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password1

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class P7UserChangeForm(UserChangeForm):
    class Meta:
        fields = ("email", "password")
        model = get_user_model()

