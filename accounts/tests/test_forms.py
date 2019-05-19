from datetime import date

from django.test import TestCase

from accounts.forms import UserProfileForm


class UserProfileFormTest(TestCase):

    def setUp(self):
        self.required_form_fields = [
            'date_of_birth',
            'bio',
        ]

        self.optional_form_fields = [
            'given_name',
            'family_name',
            'city',
            'state',
            'country',
            'favourite_animal',
            'hobby',
            'favourite_fountain_pen',
        ]

        self.excluded_form_fields = [
            'user',  # provided by looking up active user in request
            'avatar',  # dedicated page for editing
        ]

        self.valid_date = date(1977, 5, 25)
        self.valid_bio = "this is a string with more than 10 characters"
        self.invalid_bio = "too short"

    def test_form_renders_inputs(self):
        form = UserProfileForm()
        expected_inputs = self.required_form_fields + self.optional_form_fields

        rendered_form = form.as_p()
        
        for field in expected_inputs:
            self.assertIn(f'id_{field}', rendered_form)

    def test_form_fails_validation_if_required_items_missing(self):
        no_dob_form = UserProfileForm(
            data={'date_of_birth': None, 'bio': self.valid_bio}
        )
        no_bio_form = UserProfileForm(
            data={'date_of_birth': self.valid_date, 'bio': ''}
        )

        for form in [no_dob_form, no_bio_form]:
            self.assertFalse(form.is_valid())

    def test_valid_bio_passes_validation(self):
        # A valid bio must have at least 10 characters
        form = UserProfileForm(
            data={'date_of_birth': self.valid_date, 'bio': self.valid_bio}
        )

        self.assertTrue(form.is_valid())

    def test_invalid_bio_fails_validation(self):
        form = UserProfileForm(
            data={'date_of_birth': self.valid_date, 'bio': self.invalid_bio}
        )

        self.assertFalse(form.is_valid())
