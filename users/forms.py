from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (UserCreationForm,
                                       UserChangeForm,
                                       ReadOnlyPasswordHashField)

# The following imports are for PasswordChangeForm
from django.contrib.auth import password_validation
# (https://github.com/django/django/blob/master/django/contrib/auth/password_validation.py)

# The following imports are for custom validators
import re
from django.core.exceptions import ValidationError


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
    password = ReadOnlyPasswordHashField(widget=forms.HiddenInput())
    confirm_email = forms.EmailField(label="Confirm Email")

    class Meta:
        fields = ("email", "password")
        model = get_user_model()
    
    def __init__(self, *args, **kwargs):
        self.field_order = ['email', 'confirm_email']
        super().__init__(*args, **kwargs)

    def clean_password(self):
        return self.initial["password"]
    
    def clean_confirm_email(self):
        email1 = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('confirm_email')
        if email1 != email2:
            raise forms.ValidationError("Emails don't match")
        return email1


# Begin Password Validation
# -------------------------
# Custom Validators
class OtherIdentityAttributesValidator(object):
    """Check that password doesn't contain any other identity components of
    the user (username [here email], first name or last name)
    """
    error_msg = {
        'code': 'other_identity_component',
        'message': ("You may not include your username, first name or last "
                    "name in your password")
    }

    def validate(self, password, user=None):
        forbidden_words = []
        if user:
            forbidden_words.append(user.email.lower())
            if hasattr(user, 'userprofile'):
                forbidden_words.append(user.userprofile.given_name.lower())
                forbidden_words.append(user.userprofile.family_name.lower())

        for word in forbidden_words:
            if word in password.lower():
                raise ValidationError(self.error_msg['message'], self.error_msg['code'])

    def get_help_text(self):
        return self.error_msg['message']


class ContentsValidator(object):
    """Check that the password contains the specified characters"""
    error_msg = {
        'code': '',
        'message': ''
    }
    pattern = r''
    def validate(self, password, user=None):
        if not re.search(self.pattern, password):
            raise ValidationError(self.error_msg['message'], self.error_msg['code'])

    def get_help_text(self):
        return self.error_msg['message']


class NumericValidator(ContentsValidator):
    """Check that there is at least one digit character in the password"""
    error_msg = {
        'code': 'no_number',
        'message': 'Your password must contain at least 1 number'
    }
    pattern = r'\d'


class LowerCaseValidator(ContentsValidator):
    """Check that there is at least one lowercase character in the password"""
    error_msg = {
        'code': 'no_lowercase',
        'message': 'Your password must contain at least 1 lowercase letter'
    }
    pattern = r'[a-z]'


class UpperCaseValidator(ContentsValidator):
    """Check that there is at least one uppercase character in the password"""
    error_msg = {
        'code': 'no_uppercase',
        'message': 'Your password must contain at least 1 uppercase letter'
    }
    pattern = r'[A-Z]'


class SpecialCharacterValidator(ContentsValidator):
    """Check that there is at least one special character in the password"""
    error_msg = {
        'code': 'no_special',
        'message': 'Your password must contain at least 1 special character'
    }
    """
    note that inside a set the only characters that need to be escaped
    are ], -, ^
    (https://github.com/tartley/python-regex-cheatsheet/blob/master/cheatsheet.rst)
    per regex101, " is also a character that needs escaping inside a set
    and \ has to be escaped to be recognised as a literal
    what about &, is the form providing & or &amp; ?
    """
    pattern = r'[~`!@#$%\^&*()\-_+=[\]{}|\\:;\'\",<.>?/]'


# Password Change Form
class PasswordChangeForm(forms.Form):
    """A form that lets a user change their password
    (based on the builtin version from Django)
    """
    error_messages = {
        'password_incorrect': "The existing password you entered was not valid",
        'password_mismatch': "The two password fields didn't match",
        'password_same_as_old': "The new password must differ from the old password",
    }

    old_password = forms.CharField(
        label="Current Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True})
    )
    new_password1 = forms.CharField(
        label="New Password",
        strip=False,
        widget=forms.PasswordInput(),
        help_text=password_validation.password_validators_help_text_html()
    )
    new_password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput()
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """Validate that the old password field is correct."""
        old_password = self.cleaned_data.get("old_password")
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code="password_incorrect",
            )
        return old_password

    def clean_new_password1(self):
        """Validate that the new password meets our password rules"""
        new_password = self.cleaned_data.get("new_password1")
        # password_validation.validate_password returns None if valid or
        # a list of errors if there are any
        password_validation.validate_password(
            new_password,
            user=self.user,
        )
        return new_password
    
    def clean_new_password2(self):
        old_password = self.cleaned_data.get("old_password")
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch'
            )
        if password1 == old_password:
            raise forms.ValidationError(
                self.error_messages['password_same_as_old'],
                code='password_same_as_old'
            )
        return password2

    def save(self, commit=True):
        password = self.cleaned_data.get("new_password1")
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user