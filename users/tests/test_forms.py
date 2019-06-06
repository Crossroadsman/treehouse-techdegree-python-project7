from datetime import date

from django.test import TestCase

from django.contrib.auth import get_user_model, get_user
User = get_user_model()

from django.core.exceptions import ValidationError

from accounts.models import UserProfile
from users.forms import (P7UserCreationForm, P7UserChangeForm, 
                         PasswordChangeForm, OtherIdentityAttributesValidator,
                         ContentsValidator, NumericValidator, 
                         UpperCaseValidator, LowerCaseValidator,
                         SpecialCharacterValidator)


# Forms
# -----
class P7UserCreationFormTestCase(TestCase):
    
    def test_form_with_valid_inputs_passes_validation(self):
        test_inputs = {
            'password1': 'ValidPass123456,./',
            'password2': 'ValidPass123456,./',
            'email': 'alicesmith@test.com'
        }

        form = P7UserCreationForm(data=test_inputs)

        self.assertTrue(form.is_valid())

    def test_form_fails_validation_if_user_exists(self):
        test_inputs = {
            'password1': 'ValidPass123456,./',
            'password2': 'ValidPass123456,./',
            'email': 'alicesmith@test.com'
        }

        User.objects.create_user(email=test_inputs['email'], password=test_inputs['password1'])

        form = P7UserCreationForm(data=test_inputs)

        self.assertFalse(form.is_valid())


class P7UserChangeFormTestCase(TestCase):
    
    def test_form_with_valid_inputs_passes_validation(self):
        test_inputs = {
            'password': 'ValidPass123456,./',
            'email': 'bobjones@test.com',  # new email
            'confirm_email': 'bobjones@test.com'
        }

        form = P7UserChangeForm(data=test_inputs)

        self.assertTrue(form.is_valid())

    def test_form_fails_validation_if_emails_dont_match(self):
        test_inputs = {
            'password': 'ValidPass123456,./',
            'email': 'bobjones@test.com',  # new email
            'confirm_email': 'carolrivest@test.com'
        }

        User.objects.create_user(email=test_inputs['email'], password=test_inputs['password1'])

        form = P7UserChangeForm(data=test_inputs)

        self.assertFalse(form.is_valid())


class PasswordChangeFormTestCase(TestCase):

    def setUp(self):
        self.old_password = 'ValidPass123456,./'
        self.user = User.objects.create_user(
            email='alicesmith@test.com',
            password=self.old_password
        )

    def test_form_with_valid_inputs_passes_validation(self):
        test_inputs = {
            'old_password': self.old_password,
            'new_password1': 'NewValidPass7890!@#',
            'new_password2': 'NewValidPass7890!@#',
        }

        form = PasswordChangeForm(user=self.user, data=test_inputs)

        self.assertTrue(form.is_valid())

    def test_form_fails_validation_if_passwords_dont_match(self):
        test_inputs = {
            'old_password': self.old_password,
            'new_password1': 'NewValidPass7890!@#',
            'new_password2': 'OtherValidPass7890!@#',
        }

        form = PasswordChangeForm(user=self.user, data=test_inputs)

        self.assertFalse(form.is_valid())

    def test_form_fails_validation_if_old_password_wrong(self):
        test_inputs = {
            'old_password': 'TheWrongPassword',
            'new_password1': 'NewValidPass7890!@#',
            'new_password1': 'NewValidPass7890!@#',
        }

        form = PasswordChangeForm(user=self.user, data=test_inputs)

        self.assertFalse(form.is_valid())
    

# Validators
# ----------
class OtherIdentityAttributesValidatorTestCase(TestCase):
    def setUp(self):
        self.test_credentials = {
            'email': "alicesmith@test.com",
            'password': "Testing123xyz!,.",
        }
        self.user = User.objects.create_user(**self.test_credentials)
        self.userprofile_fields = {
            'user': self.user,
            'date_of_birth': date(1977, 5, 25),
            'bio': "this is a string with more than 10 characters"
        }
        self.userprofile_optional_fields = {
            'family_name': 'smith',
            'given_name': 'alice'
        }
        UserProfile.objects.create(
            **{
                **self.userprofile_fields,
                **self.userprofile_optional_fields
            }
        )

        self.invalid_words = {
            'username': self.user.email,
            'family_name': self.user.userprofile.family_name,
            'given_name': self.user.userprofile.given_name
        }

        self.valid_suffix = "Ul123456,./"

        self.validator = OtherIdentityAttributesValidator()

    def test_valid_string_passes_validation(self):
        test_password = "bobjones" + self.valid_suffix

        self.assertIsNone(self.validator.validate(test_password, self.user))

    def test_invalid_username_fails_validation(self):

        test_password = self.invalid_words['username'] + self.valid_suffix

        with self.assertRaises(ValidationError):
            self.validator.validate(test_password, self.user)

    def test_invalid_family_name_fails_validation(self):

        test_password = self.invalid_words['family_name'] + self.valid_suffix

        with self.assertRaises(ValidationError):
            self.validator.validate(test_password, self.user)

    def test_invalid_given_name_fails_validation(self):

        test_password = self.invalid_words['given_name'] + self.valid_suffix

        with self.assertRaises(ValidationError):
            self.validator.validate(test_password, self.user)


class ContentsValidatorTestCase(TestCase):
    pass


class SimpleValidatorTestCase(TestCase):
    def setUp(self):
        self.abstract = True
        self.valid_input = 'UPPERlower123456,./$%^'
        self.invalid_input = None

        self.validator = None

    def test_valid_string_passes_validation(self):
        if self.abstract:
            return
        
        test_password = self.valid_input

        self.assertIsNone(self.validator.validate(test_password))

    def test_invalid_string_fails_validation(self):
        if self.abstract:
            return
        
        test_password = self.invalid_input

        with self.assertRaises(ValidationError):
            self.validator.validate(test_password)

class NumericValidatorTestCase(SimpleValidatorTestCase):

    def setUp(self):
        super().setUp()

        self.abstract = False
        self.invalid_input = 'UPPERlower,./$%^'
        self.validator = NumericValidator()


class LowerCaseValidatorTestCase(SimpleValidatorTestCase):

    def setUp(self):
        super().setUp()

        self.abstract = False
        self.invalid_input = 'UPPER123456,./$%^'
        self.validator = LowerCaseValidator()


class UpperCaseValidatorTestCase(SimpleValidatorTestCase):

    def setUp(self):
        super().setUp()

        self.abstract = False
        self.invalid_input = 'lower123456,./$%^'
        self.validator = UpperCaseValidator()


class SpecialCharacterTestCase(SimpleValidatorTestCase):

    def setUp(self):
        super().setUp()

        self.abstract = False
        self.invalid_input = 'UPPERlower123456'
        self.validator = SpecialCharacterValidator()
