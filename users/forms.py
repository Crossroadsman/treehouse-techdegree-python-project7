from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (UserCreationForm,
                                       UserChangeForm)


# The purpose of this class is to override the builtin version so that
# we can customise it. In this case we are:
# - adding an email address field (and setting the label text for the email
#   field)
class P7UserCreationForm(UserCreationForm):
    class Meta:
        fields = ("email", "password1", "password2")
        model = get_user_model()
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email']
    '''


class P7UserChangeForm(UserChangeForm):
    class Meta:
        fields = ("email", "old_password", "password1", "password2")
        model = get_user_model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = "Old Password"
        self.fields['password1'].label = "New Password"
        self.fields['password2'].label = "New Password Again"
